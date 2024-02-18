from lyzr_automata.agents.agent_base import Agent
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata.ai_models.perplexity import PerplexityModel
from lyzr_automata.pipelines.linear_sync_pipeline import LinearSyncPipeline
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.tasks.task_base import Task
from lyzr_automata.tasks.util_tasks import summarize_task
from lyzr_automata.tools.prebuilt_tools import linkedin_image_text_post_tool

# Create model instances as per your requirements
# Use prebuilt models for perplexity and OpenAI directly as needed
# Extend the AIModel base class for custom model integration


def run_automated_linkedin_post_pipeline(
    perplexity_api_key: str,
    open_ai_api_key: str,
    linkedin_owner: str,
    linkedin_token: str,
):
    # Define the models and tools
    perplexity_model_text = PerplexityModel(
        api_key=perplexity_api_key,
        parameters={
            "model": "pplx-70b-online",
        },
    )
    open_ai_model_text = OpenAIModel(
        api_key=open_ai_api_key,
        parameters={
            "model": "gpt-4-turbo-preview",
            "temperature": 0.2,
            "max_tokens": 1500,
        },
    )
    open_ai_model_image = OpenAIModel(
        api_key=open_ai_api_key,
        parameters={
            "n": 1,
            "model": "dall-e-3",
        },
    )

    # Define agents
    content_researcher_agent = Agent(
        prompt_persona="You are an AI journalist good at using the provided data and write an engaging article",
        role="AI Journalist",
    )
    linkedin_content_writer_agent = Agent(
        prompt_persona="You write engaging linkedin posts with the provided input data",
        role="Linkedin Content Creator",
    )

    # Define a custom tool for LinkedIn posts
    linkedin_post_tool = linkedin_image_text_post_tool(
        owner=linkedin_owner, token=linkedin_token
    )

    # Define tasks
    search_task = Task(
        name="Search Latest AI News",
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=perplexity_model_text,
        instructions="Search and collect all latest news about the startup Perplexity",
        log_output=True,
    )

    research_task = Task(
        name="Draft Content Creator",
        agent=content_researcher_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Analyze the input and clean the data and write a summary of 1000 words which can be used to create Linkedin post in the next task",
        enhance_prompt=False,
    )
    linkedin_content_writing_task = Task(
        name="Linkedin Post Creator",
        agent=linkedin_content_writer_agent,
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=open_ai_model_text,
        instructions="Use the news summary provided and write 1 engaging linkedin post of 200 words",
        log_output=True,
        enhance_prompt=False,
    )

    image_creation_task = Task(
        name="linkedin image creation",
        output_type=OutputType.IMAGE,
        input_type=InputType.TEXT,
        model=open_ai_model_image,
        log_output=True,
        instructions="Use the research material provided and create a linkedin post image that would be suitable for posting",
    )

    linkedin_upload_task = Task(
        name="upload post to linkedin",
        model=open_ai_model_text,
        tool=linkedin_post_tool,
        instructions="Post on Linkedin",
        input_tasks=[linkedin_content_writing_task, image_creation_task],
    )

    # Define and run the pipeline
    pipeline = LinearSyncPipeline(
        name="Automated Linkedin Post",
        completion_message="Posted Successfully 🎉",
        tasks=[
            search_task,
            research_task,
            linkedin_content_writing_task,
            # Note: summarize_task is not defined in the original script, so it's commented out.
            summarize_task(15, text_ai_model=open_ai_model_text),
            image_creation_task,
            linkedin_upload_task,
        ],
    )
    pipeline.run()
