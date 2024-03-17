import identity
import identity.web
import requests
from flask import Flask, redirect, render_template, request, session, url_for
from flask_session import Session
from bs4 import BeautifulSoup

from helpers import email_sender_function, email_draft_function

import app_config

app = Flask(__name__)
app.config.from_object(app_config)
Session(app)

from werkzeug.middleware.proxy_fix import ProxyFix

app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)

auth = identity.web.Auth(
    session=session,
    authority=app.config.get("AUTHORITY"),
    client_id=app.config["CLIENT_ID"],
    client_credential=app.config["CLIENT_SECRET"],
)


@app.route("/login")
def login():
    return render_template(
        "login.html",
        version=identity.__version__,
        **auth.log_in(
            scopes=app_config.SCOPE,  # Have user consent to scopes during log-in
            redirect_uri=url_for(
                "auth_response", _external=True
            ),  # Optional. If present, this absolute URL must match your app's redirect_uri registered in Azure Portal
        )
    )


@app.route(app_config.REDIRECT_PATH)
def auth_response():
    result = auth.complete_log_in(request.args)
    if "error" in result:
        return render_template("auth_error.html", result=result)
    return redirect(url_for("index"))


@app.route("/logout")
def logout():
    return redirect(auth.log_out(url_for("index", _external=True)))


@app.route("/", methods=["GET", "POST"])
def index():
    if not (app.config["CLIENT_ID"] and app.config["CLIENT_SECRET"]):
        return render_template("config_error.html")
    if not auth.get_user():
        return redirect(url_for("login"))

    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))

    if request.method == "POST":
        video_link = request.form["video_link"]
        transcribed_email, email_list = summarise_video(video_link, token)
        summary = html_parser(transcribed_email)

        return render_template(
            "index.html",
            video_link=video_link,
            summary=summary,
            transcribed_email=transcribed_email,
            email_list=email_list,
            user=auth.get_user(),
            version=identity.__version__,
        )

    return render_template(
        "index.html", user=auth.get_user(), version=identity.__version__
    )


@app.route("/email_summary", methods=["POST"])
def email_summary():
    token = auth.get_token_for_user(app_config.SCOPE)
    if "error" in token:
        return redirect(url_for("login"))

    transcribed_email = request.form["transcribed_email"]
    email_list = request.form["email_list"]
    final_output = send_email(transcribed_email, email_list)

    if final_output["sent"]:
        return render_template(
            "email_success.html", user=auth.get_user(), version=identity.__version__
        )

    return render_template(
        "index.html", user=auth.get_user(), version=identity.__version__
    )


# IMPORTANT FUNCTIONS
def get_meeting_id(meeting_url, token):
    endpoint = "https://graph.microsoft.com/v1.0/me/onlineMeetings?$filter=JoinWebUrl%20eq%20'{meetingURL}'".format(
        meetingURL=meeting_url
    )
    api_result = requests.get(
        endpoint,
        headers={"Authorization": "Bearer " + token["access_token"]},
        timeout=30,
    ).json()

    meeting_ID = api_result["value"][0]["id"]
    return meeting_ID


def get_max_attendees_report(meeting_ID, token):
    endpoint2 = "https://graph.microsoft.com/v1.0/me/onlineMeetings/{meeting}/attendanceReports".format(
        meeting=meeting_ID
    )
    api_result2 = requests.get(
        endpoint2,
        headers={"Authorization": "Bearer " + token["access_token"]},
        timeout=30,
    ).json()

    max_count = 0
    for unique_meets in api_result2["value"]:
        if unique_meets["totalParticipantCount"] > max_count:
            report_ID = unique_meets["id"]
            max_count = unique_meets["totalParticipantCount"]

    return report_ID


def get_attendees_list(meeting_ID, report_ID, token):
    endpoint3 = "https://graph.microsoft.com/v1.0/me/onlineMeetings/{meeting}/attendanceReports/{report}/attendanceRecords".format(
        meeting=meeting_ID, report=report_ID
    )
    api_result3 = requests.get(
        endpoint3,
        headers={"Authorization": "Bearer " + token["access_token"]},
        timeout=30,
    ).json()

    attendance_values = api_result3["value"]
    email_list = []
    for attendee in attendance_values:
        if attendee["emailAddress"]:
            email_list.append(attendee["emailAddress"])

    return email_list


def get_transcript_ID(meeting_ID, token):
    endpoint = "https://graph.microsoft.com/v1.0/me/onlineMeetings/{meeting}/transcripts".format(
        meeting=meeting_ID
    )
    api_result = requests.get(
        endpoint,
        headers={"Authorization": "Bearer " + token["access_token"]},
        timeout=30,
    ).json()

    transcript_ID = api_result["value"][0]["id"]
    return transcript_ID


def get_transcript_content(meeting_ID, transcript_ID, token):
    endpoint2 = "https://graph.microsoft.com/v1.0/me/onlineMeetings/{meeting}/transcripts/{transcript}/content?$format=text/vtt".format(
        meeting=meeting_ID, transcript=transcript_ID
    )
    api_result2 = requests.get(
        endpoint2,
        headers={"Authorization": "Bearer " + token["access_token"]},
        timeout=30,
    ).text

    return api_result2


def html_parser(html_content):
    # Find the table
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    return table


def send_email(summary, email_list):
    return email_sender_function(summary, email_list)


def summarise_video(meeting_url, token):
    meeting_ID = get_meeting_id(meeting_url, token)

    # FIND REPORT ID
    report_ID = get_max_attendees_report(meeting_ID, token)

    # FIND ATTENDEES
    email_list = get_attendees_list(meeting_ID, report_ID, token)

    # FIND TRANSCRIPT ID
    transcript_ID = get_transcript_ID(meeting_ID, token)

    # GET TRANSCRIPT CONTENT
    transcript_content = get_transcript_content(meeting_ID, transcript_ID, token)

    # SUMMARIZE TRANSCRIPT
    transcribed_email = email_draft_function(transcript_content)

    return transcribed_email, email_list


if __name__ == "__main__":
    app.run(debug=True)
