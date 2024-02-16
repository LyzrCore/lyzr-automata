![version](https://img.shields.io/badge/version-0.1.1-blue.svg) [![Discord](https://img.shields.io/badge/Discord-join%20now-blue.svg?style=flat&logo=Discord)](https://discord.gg/dXmgggHYUz) [![YouTube Video](https://img.shields.io/badge/YouTube-Video-red?logo=youtube)](https://youtu.be/6U42TgaR6RA?feature=shared)


![Lyzr Automata Banner](https://github.com/LyzrCore/lyzr-automata/assets/136654928/2f05f718-5526-4178-a312-90059b945e23)

# Lyzr Automata 0.1.1
### A low-code multi-agent automation framework.

Note : Framework was developed swiftly as an experiment, leading to initial imperfections. We're committed to enhancing its stability and structure in upcoming releases, ensuring a high-quality. We encourage contributions from everyone, aiming to advance the project further together.

### Lyzr Automata - Autonomous Multi-Agent Framework for Process Automation
Lyzr Automata is a sophisticated multi-agent automation framework designed to keep things simple, with a focus on workflow efficiency and effectiveness. It enables the creation of multiple agents that are coupled with specific tasks. The agents and tasks can run independently and complete the provided instructions, thus entering a stable state.

![Lyzr Automata](https://github.com/LyzrCore/lyzr-automata/assets/136654928/a9f0ecf7-0722-4038-8e3a-f00ce43c882e)

### How to Install
Get started with Lyzr Automata by installing the package using pip:
```bash 
pip install lyzr-automata=0.1.1 
```
### Linkedin post automation example

```python
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

perplexity_model_text = PerplexityModel(
    api_key="YOUR_API_KEY",
    parameters={
        "model": "pplx-70b-online",
    },
)
open_ai_model_text = OpenAIModel(
    api_key="YOUR_API_KEY",
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.2,
        "max_tokens": 1500,
    },
)
open_ai_model_image = OpenAIModel(
    api_key="YOUR_API_KEY",
    parameters={
        "n": 1,
        "model": "dall-e-3",
    },
)

# Create custom role and persona based agents using Agent class

content_researcher_agent = Agent(
    prompt_persona="You are an AI journalist good at using the provided data and write an engaging article",
    role="AI Journalist",
)
linkedin_content_writer_agent = Agent(
    prompt_persona="You write engaging linkedin posts with the provided input data",
    role="Linkedin Content Creator",
)

# Use prebuilt linkedin post tool
# You can create your own custom tools with our base Tool class

linkedin_post_tool = linkedin_image_text_post_tool(
    owner="",
    token=""
)

# Create tasks for your pipeline using Task class

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

# Currently we support only sync linear pipeline
# Use LinearSyncPipeline class to run linear pipelines
# Async DAG workflow & Human-in-Loop review are on our feature pipeline for the next versions

def main():
    LinearSyncPipeline(
        name="Automated Linkedin Post",
        completion_message="Posted Successfully 🎉",
        tasks=[
            search_task,
            research_task,
            linkedin_content_writing_task,
            summarize_task(15, text_ai_model=open_ai_model_text),
            image_creation_task,
            linkedin_upload_task,
        ],
    ).run()


main()
```
Colab Notebook: https://colab.research.google.com/drive/1lVJrdjHVZjbwZSqwJEU_etHC4GM3ihD0?usp=sharing

[![Discord](https://img.shields.io/badge/Discord-join%20now-blue.svg?style=flat&logo=Discord)](https://discord.gg/dXmgggHYUz)

## Contact
For queries, reach us at contact@lyzr.ai

## Demo

[![Alt text](https://github.com/LyzrCore/lyzr-automata/assets/136654928/5cd11388-dd44-41b3-a447-228d07e9f523)](https://youtu.be/6U42TgaR6RA?feature=shared)

