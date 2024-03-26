from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata import Agent, Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.pipelines.linear_sync_pipeline  import  LinearSyncPipeline
from lyzr_automata import Logger

from dotenv import load_dotenv
import os

load_dotenv()

# LOAD OUR API KEY
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# DALLE 3 Image Model
open_ai_model_image = OpenAIModel(
    api_key=OPENAI_API_KEY,
    parameters={
        "n": 1,
        "model": "dall-e-3",
    },
)

# GPT 4 Text Model
open_ai_model_text = OpenAIModel(
    api_key= OPENAI_API_KEY,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.5,
        "max_tokens": 1500,
    },
)

def storyboard_generator(input_content):
    # Screenplay Writer Agent
    screenplay_writer_agent = Agent(
        prompt_persona="You are an intelligent Screenplay writer good at writing a short and detailed scene",
        role="Screenplay writer",
    )

    # Write Screenplay Task
    screenplay_content_task = Task(
        name="Screenplay Content Creator",
        agent=screenplay_writer_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Use the scene description provided and write a scene for a movie in 200 words. Use your creativity. [IMPORTANT!] Setup the location and characters in a detailed manner",
        log_output=True,
        enhance_prompt=False,
        default_input=input_content
    )

    # Generate Storyboard
    storyboard_creation_task = Task(
        name="Storyboard Image Creation",
        output_type=OutputType.IMAGE,
        input_type=InputType.TEXT,
        model=open_ai_model_image,
        log_output=True,
        instructions="Generate a set of 4 storyboard drawings for the given scene description. Capture every detail. Minimalistic style. [IMPORTANT!] Avoid any text or numbers in the image.",
    )

    logger = Logger()
    # Linear Pipeline to run tasks
    main_output = LinearSyncPipeline(
        logger=logger,
        name="Generate Storyboard",
        completion_message="Storyboard Generated!",
        tasks=[
            screenplay_content_task,
            storyboard_creation_task,
        ],
    ).run()

    return main_output