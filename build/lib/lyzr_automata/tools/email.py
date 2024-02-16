import smtplib
from typing import Optional
from pydantic import BaseModel
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
    username, password, receiver_emails, subject, body, host, port, sender_email
):
    """
    Send a simple plain text email to multiple recipients, automatically converting
    markdown-style bold, new lines to <br>, and URLs to clickable links in HTML without using the email package.
    Ensures UTF-8 encoding.

    Parameters:
    - username: The sender's email username.
    - password: The sender's email password.
    - receiver_emails: A list of recipient's email addresses.
    - subject: The subject of the email.
    - body: The body text of the email, with ** for bold and automatic URL conversion.
    - host: SMTP server host.
    - port: SMTP server port.
    - sender_email: The sender's email address.
    """
    # Convert markdown and other patterns to HTML
    body_html = markdown_to_html(body)
    subject_html = markdown_to_html(subject)

    # Encode subject for UTF-8 headers (might need refinement for actual use)
    subject_encoded = subject_html

    # Create HTML message with UTF-8 encoding
    message = f"From: {sender_email}\nTo: {','.join(receiver_emails)}\nSubject: {subject_encoded}\nMIME-Version: 1.0\nContent-type: text/html; charset=utf-8\n\n{body_html}"

    try:
        server = smtplib.SMTP(host, port)
        server.starttls()
        server.login(username, password)
        # Convert entire message to UTF-8 before sending
        server.sendmail(sender_email, receiver_emails, message.encode("utf-8"))
        return {"sent": True, "receiver_emails": receiver_emails}
    except Exception as e:
        print(f"Failed to send email: {e}")
        return {"sent": False, "receiver_emails": receiver_emails}
    finally:
        server.quit()


class EmailSenderInput(BaseModel):
    receiver_emails: list[str]
    subject: str
    body: str


class EmailSenderOutput(BaseModel):
    sent: bool
    receiver_emails: list[str]
