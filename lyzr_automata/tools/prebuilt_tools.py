from lyzr_automata.tools.email import (
    EmailSenderInput,
    EmailSenderOutput,
    send_email_by_smtplib,
)
from lyzr_automata.tools.linkedin import (
    LinkedInPostInput,
    LinkedInPostOutput,
    post_image_and_text,
)

from lyzr_automata.tools.devto import (
    DevToArticleInput,
    DevToArticleOutput,
    create_devto_article
)

from lyzr_automata.tools.tool_base import Tool


def linkedin_image_text_post_tool(owner: str, token: str):
    return Tool(
        name="LinkedIn Post",
        desc="Posts an post on linkedin provided details.",
        function=post_image_and_text,
        function_input=LinkedInPostInput,
        function_output=LinkedInPostOutput,
        default_params={"owner": owner, "token": token},
    )


def send_email_by_smtp_tool(username: str, password: str, host: str, port: int ,sender_email:str=None):
    if sender_email == None:
        sender_email = username
    return Tool(
        name="Email Sender",
        desc="Sends email to list of receiver emails",
        function=send_email_by_smtplib,
        function_input=EmailSenderInput,
        function_output=EmailSenderOutput,
        default_params={
            "username": username,
            "password": password,
            "host": host,
            "port": port,
            "sender_email":sender_email
        },
    )

def devto_article_post(api_key:str,published:bool):
    return Tool(
        name="dev.to article poster",
        desc="posts dev.to article",
        function=create_devto_article,
        function_input=DevToArticleInput,
        function_output=DevToArticleOutput,
        default_params={
            "api_key": api_key,
            "published": published,
        },
    )
