import smtplib
from typing import Optional
from pydantic import BaseModel
from email.utils import make_msgid, formatdate
import re


def markdown_to_html(text):
    """
    Convert markdown-style bold (**bold**), new lines to <br>, and URLs to clickable links in HTML.
    """
    # Convert bold
    bold_pattern = re.compile(r"\*\*(.*?)\*\*")
    text = bold_pattern.sub(r"<b>\1</b>", text)

    return text


def send_email_by_smtplib(
    username,
    password,
    receiver_emails,
    subject,
    body,
    host,
    port,
    sender_email,
    thread_id=None,
):  
    in_reply_to = thread_id
    # Generate a unique Message-ID
    message_id = make_msgid()

    # Convert markdown and other patterns to HTML
    body_html = markdown_to_html(body)

    # Prepare the message headers, including reply headers if provided
    headers = [
        f"From: {sender_email}",
        f"To: {','.join(receiver_emails)}",
        f"Subject: {str(subject)}",
        "MIME-Version: 1.0",
        "Content-type: text/html; charset=utf-8",
        f"Message-ID: {message_id}",
        f"Date: {formatdate(localtime=True)}",
    ]
    if in_reply_to:
        headers.append(f"In-Reply-To: {in_reply_to}")
        headers.append(f"References: {in_reply_to}")

    message = "\n".join(headers) + f"\n\n{body_html}"
    try:
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(username, password)
        server.sendmail(sender_email, receiver_emails, message.encode("utf-8"))
        return {
            "sent": True,
            "receiver_emails": receiver_emails,
            "message_id": message_id,
            "subject": subject,
            "body":body_html,
        }
    except Exception as e:
        print(f"Failed to send email: {e}")
        return {"sent": False, "receiver_emails": receiver_emails, "message_id": None}
    finally:
        server.quit()


class EmailSenderInput(BaseModel):
    receiver_emails: list[str]
    subject: str
    body: str
    thread_id:Optional[str]


class EmailSenderOutput(BaseModel):
    sent: bool
    receiver_emails: list[str]
