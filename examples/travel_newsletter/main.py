# 1. Draft content for newsletter using GPT 4
# 2. Create an image based on the content using DALLE 3
# 3. Merge Image and Newsletter as an email
# 4. Send an email to list of email IDs

from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
PASSWORD = os.getenv("PASSWORD")
EMAIL = os.getenv("EMAIL")

from lyzr_automata.ai_models.openai import OpenAIModel

# GPT 4 Text Model
open_ai_model_text = OpenAIModel(
    api_key= OPENAI_API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)

# DALLE 3 Image Model
open_ai_model_image = OpenAIModel(
    api_key=OPENAI_API_KEY,
    parameters={
        "n": 1,
        "model": "dall-e-3",
    },
)

from lyzr_automata import Agent
from lyzr_automata import Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.tools.prebuilt_tools import send_email_by_smtp_tool

# Newsletter Writer Agent
content_researcher_agent = Agent(
    prompt_persona="You are an intelligent Travel Newsletter writer good at writing a detailed newsletter on a particular destination",
    role="Travel Newsletter writer",
)

# Draft a newsletter Task
research_task = Task(
    name="Draft Content Creator",
    agent=content_researcher_agent,
    output_type=OutputType.TEXT,
    input_type=InputType.TEXT,
    model=open_ai_model_text,
    instructions="Write a travel newsletter on Mumbai in 500 words and [IMPORTANT!] send the response in html use bullets for points and beautify it be as creative as you want.",
    log_output=True,
    enhance_prompt=False,
)

# Create an image Task
image_creation_task = Task(
    name="Newsletter Image Creation",
    output_type=OutputType.IMAGE,
    input_type=InputType.TEXT,
    model=open_ai_model_image,
    log_output=True,
    instructions="Use the travel newsletter provided and create an image that would be suitable for posting. Avoid any text in the image",
)

# Merge image and newsletter Task
merge_image_text_task = Task(
    name = "Merge Image and Email",
    model=open_ai_model_text,
    log_output=True,
    instructions="Include the image in the html code provided. Return only the HTML and CSS code",
    input_tasks = [research_task, image_creation_task]
)

# Use the prebuilt send email Tool
email_sender = send_email_by_smtp_tool(
    username=EMAIL,
    password=PASSWORD,
    host="smtp.gmail.com",
    port=587,
    sender_email=EMAIL
)

# Send email Task
send_email_task = Task(
    name = "Send Email Task",
    tool = email_sender,
    instructions="Send Email",
    model=open_ai_model_text,
    input_tasks = [merge_image_text_task],
    default_input = ['rasswanthshankar@gmail.com']
)

from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from lyzr_automata import Logger

# Linear Pipeline to run tasks
def main_program():
    logger = Logger()
    LinearSyncPipeline(
        logger=logger,
        name="Send Email",
        completion_message="Email Sent!",
        tasks=[
            research_task,
            image_creation_task,
            merge_image_text_task,
            send_email_task
        ],
    ).run()

main_program()