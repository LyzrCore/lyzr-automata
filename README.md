![version](https://img.shields.io/badge/version-0.1.0-blue.svg) [![Discord](https://img.shields.io/badge/Discord-join%20now-blue.svg?style=flat&logo=Discord)](https://discord.gg/VpQQTJ9d)


## Lyzr Automata 
##### A low-code multi-agent automation framework.

Note : Framework was developed swiftly as an experiment, leading to initial imperfections. We're committed to enhancing its stability and structure in upcoming releases, ensuring a high-quality. We encourage contributions from everyone, aiming to advance the project further together.

### Lyzr Automata - Autonomous Multi-Agent Framework for Process Automation
Lyzr Automata is a sophisticated multi-agent automation framework designed to keep things simple, with a focus on workflow efficiency and effectiveness. It enables the creation of multiple agents that are coupled with specific tasks. The agents and tasks can run independently and complete the provided instructions, thus entering a stable state.


### How to Install
Get started with Lyzr Automata by installing the package using pip:
```bash 
pip install lyzr-automata=0.1.0 
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
        "model": "mistral-7b-instruct",
    },
)
open_ai_model_text = OpenAIModel(
    api_key="YOUR_API_KEY",
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 1,
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
    prompt_persona="you were a born genius when it comes to researching content",
    role="content researcher",
)
linkedin_content_writer_agent = Agent(
    prompt_persona="you are a smart person who understands how to write good tweets for linkedin maximizing content and keeping it meaningful",
    role="Linkedin content creator",
)
utils_agent = Agent(
    prompt_persona="you are text util function who is very efficient at doing tasks efficiently",
    role="text util agent",
)

# Use prebuilt linkedin post tool
# You can create your own custom tools with our base Tool class

linkedin_post_tool = linkedin_image_text_post_tool(
    owner="",
    token=""
)

# Create tasks for your pipeline using Task class

search_task = Task(
    name="news search",
    output_type=OutputType.TEXT,
    input_type=InputType.TEXT,
    model=perplexity_model_text,
    instructions="research today's news",
    log_output=True,
)

research_task = Task(
    name="news search",
    agent=content_researcher_agent,
    output_type=OutputType.TEXT,
    input_type=InputType.TEXT,
    model=open_ai_model_text,
    instructions="Do research and pull out from the input provided",
    enhance_prompt=False,
)
linkedin_content_writing_task = Task(
    name="linkedin content writing",
    agent=linkedin_content_writer_agent,
    output_type=OutputType.TEXT,
    input_type=InputType.TEXT,
    model=open_ai_model_text,
    instructions="Use the research material provided and write 1 engaging linkedin post of 200 chars. ",
    log_output=True,
    enhance_prompt=False,

)

image_creation_task = Task(
    name="linkedin image creation",
    output_type=OutputType.IMAGE,
    input_type=InputType.TEXT,
    model=open_ai_model_image,
    log_output=True,
    instructions="Use the research material provided and create a linkedin post image.",
)
linkedin_upload_task = Task(
    name="upload post to linkedin",
    model=open_ai_model_text,
    tool=linkedin_post_tool,
    instructions="upload this post",
    input_tasks=[linkedin_content_writing_task, image_creation_task],
)

# Currently we support only sync linear pipeline
# Use LinearSyncPipeline class to run linear pipelines
# Async DAG workflow is in our feature pipeline for next versions

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

## Contact
For queries, reach us at contact@lyzr.ai
