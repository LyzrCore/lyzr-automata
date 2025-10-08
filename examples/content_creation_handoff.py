"""
Advanced Handoff Example: Content Creation Workflow

This example demonstrates a complex workflow where multiple specialized agents
collaborate to create content:
1. Research Agent - Gathers information and facts
2. Writer Agent - Creates the content
3. Editor Agent - Reviews and improves the content
4. SEO Agent - Optimizes for search engines

The agents can hand off to each other based on the stage of content creation.
"""

from lyzr_automata import Agent
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata.pipelines.handoff_pipeline import HandoffPipeline, AgentConfig
import os

# Set up your OpenAI API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Please set OPENAI_API_KEY environment variable")
    exit(1)

# Create the AI model
model = OpenAIModel(
    api_key=api_key,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.5,
        "max_tokens": 1500,
    },
)

# Define specialized content creation agents

researcher = Agent(
    role="Research Analyst",
    prompt_persona="""You are an expert research analyst. You gather comprehensive information,
    verify facts, and provide detailed research on any topic. After completing research,
    you typically hand off to the writer by saying 'HANDOFF: writer'."""
)

writer = Agent(
    role="Content Writer",
    prompt_persona="""You are a creative and engaging content writer. You take research and
    transform it into compelling, well-structured content. After writing, you hand off
    to the editor by saying 'HANDOFF: editor'."""
)

editor = Agent(
    role="Content Editor",
    prompt_persona="""You are a meticulous content editor. You review content for clarity,
    grammar, structure, and flow. You make improvements and ensure quality. After editing,
    you hand off to SEO specialist by saying 'HANDOFF: seo_specialist'."""
)

seo_specialist = Agent(
    role="SEO Specialist",
    prompt_persona="""You are an SEO expert. You optimize content for search engines by
    adding keywords, meta descriptions, and ensuring proper structure. You provide the
    final optimized version of the content."""
)

# Configure agents
agent_configs = [
    AgentConfig(
        agent=researcher,
        agent_id="researcher",
        capabilities="Conducts research, gathers facts, analyzes information, provides data and insights on topics"
    ),
    AgentConfig(
        agent=writer,
        agent_id="writer",
        capabilities="Creates engaging content, writes articles, develops narratives, structures information clearly"
    ),
    AgentConfig(
        agent=editor,
        agent_id="editor",
        capabilities="Reviews content, improves clarity, fixes grammar, enhances structure and flow"
    ),
    AgentConfig(
        agent=seo_specialist,
        agent_id="seo_specialist",
        capabilities="Optimizes content for SEO, adds keywords, creates meta descriptions, improves searchability"
    ),
]

# Create the handoff pipeline
content_pipeline = HandoffPipeline(
    name="Content Creation Pipeline",
    router_model=model,
    agent_configs=agent_configs,
    default_agent_id="researcher",  # Start with research
    max_handoffs=10,  # Allow multiple handoffs for the workflow
    enable_auto_routing=True,
)

# Run the content creation workflow
print("="*80)
print("CONTENT CREATION WORKFLOW WITH AGENT HANDOFFS")
print("="*80)
print()

topic = "The Future of Artificial Intelligence in Healthcare"

result = content_pipeline.run(
    initial_request=f"""I need to create a comprehensive blog post about: '{topic}'.

    Please follow this workflow:
    1. Research the topic thoroughly
    2. Write an engaging article based on the research
    3. Edit and improve the content
    4. Optimize for SEO

    Start with research.""",
    model=model,
)

# Display results
print("\n" + "="*80)
print("WORKFLOW RESULTS")
print("="*80)

print(f"\nFinal Content:\n{result['final_response']}")
print(f"\n{'='*80}")
print(f"Execution Time: {result['execution_time']:.2f} seconds")
print(f"Total Handoffs: {result['total_handoffs']}")

print(f"\n{'='*80}")
print("HANDOFF SEQUENCE:")
print("="*80)
for i, handoff in enumerate(result['handoff_history'], 1):
    print(f"{i}. {handoff['from']} -> {handoff['to']}")
    if handoff['reason']:
        print(f"   Reason: {handoff['reason']}")

print(f"\n{'='*80}")
print("ALL AGENT RESPONSES:")
print("="*80)
for i, response_data in enumerate(result['all_responses'], 1):
    print(f"\n{i}. Agent: {response_data['agent_id']}")
    print(f"   Response: {response_data['response'][:200]}...")  # Show first 200 chars

# Example of manual workflow control
print("\n\n" + "="*80)
print("MANUAL WORKFLOW CONTROL EXAMPLE")
print("="*80)

# Create a new pipeline for manual control
manual_pipeline = HandoffPipeline(
    name="Manual Content Pipeline",
    router_model=model,
    agent_configs=agent_configs,
    default_agent_id="researcher",
    enable_auto_routing=False,  # Disable auto-routing for manual control
)

# Step 1: Research
print("\n--- Step 1: Research ---")
research_result = manual_pipeline.run_with_agent(
    agent_id="researcher",
    request="Research the key benefits of AI in medical diagnosis",
    model=model,
)
print(f"Research: {research_result[:150]}...")

# Step 2: Write
print("\n--- Step 2: Writing ---")
write_result = manual_pipeline.run_with_agent(
    agent_id="writer",
    request="Write a compelling introduction paragraph about AI in medical diagnosis based on the research above",
    model=model,
)
print(f"Draft: {write_result[:150]}...")

# Step 3: Edit
print("\n--- Step 3: Editing ---")
edit_result = manual_pipeline.run_with_agent(
    agent_id="editor",
    request="Edit and improve the introduction paragraph above",
    model=model,
)
print(f"Edited: {edit_result[:150]}...")

print("\n" + "="*80)
print("Manual workflow completed!")
print(f"Total steps in conversation: {len(manual_pipeline.context.messages)}")
