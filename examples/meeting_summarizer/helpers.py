import app_config

OPENAI_API_KEY = app_config.OPENAI_API_KEY
EMAIL = app_config.EMAIL
PASSWORD = app_config.PASSWORD

from lyzr_automata.ai_models.openai import OpenAIModel

# GPT 4 Text Model
open_ai_model_text = OpenAIModel(
    api_key=OPENAI_API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

from lyzr_automata import Agent
from lyzr_automata import Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.tools.prebuilt_tools import send_email_by_smtp_tool

summarizer_agent = Agent(
    prompt_persona="You are an intelligent agent that can summarize WebVTT content into a meaninful summary",
    role="WebVTT summarizer",
)


def email_draft_function(input_transcript):
    # Draft a summary Task
    summarize_content_task = Task(
        name="Transcript summarizer",
        agent=summarizer_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Summarize the WebVTT input into a meaningful Minutes of Meeting that captures immportant details and speakers. Return only the speaker name and their corresponding suammary [!IMPORTANT] Use HTML table to revise the email and beautify it",
        log_output=True,
        enhance_prompt=False,
        default_input=input_transcript,
    ).execute()

    return summarize_content_task


def email_sender_function(summary, email_list):
    email_sender = send_email_by_smtp_tool(
        username=EMAIL,
        password=PASSWORD,
        host="smtp.gmail.com",
        port=587,
        sender_email=EMAIL,
    )

    # Send email Task
    send_email_task = Task(
        name="Send Email Task",
        tool=email_sender,
        instructions="Send Email",
        model=open_ai_model_text,
        input_tasks=[summary],
        default_input=email_list,
        previous_output=summary,
    ).execute()

    return send_email_task
