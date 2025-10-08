"""
Example demonstrating the HandoffPipeline for automatic agent routing.

This example shows how to create a multi-agent system where:
1. A customer service agent handles general inquiries
2. A technical support agent handles technical issues
3. A sales agent handles product and pricing questions

The router automatically hands off requests to the appropriate agent.
"""

from lyzr_automata import Agent
from lyzr_automata.ai_models.openai import OpenAIModel
from lyzr_automata.pipelines.handoff_pipeline import HandoffPipeline, AgentConfig
import os

# Set up your OpenAI API key
# os.environ["OPENAI_API_KEY"] = "your-api-key-here"
# OR
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("Please set OPENAI_API_KEY environment variable")
    exit(1)

# Create the router model (used for routing decisions and task execution)
router_model = OpenAIModel(
    api_key=api_key,
    parameters={
        "model": "gpt-4-turbo-preview",
        "temperature": 0.3,
        "max_tokens": 1000,
    },
)

# Define specialized agents

# 1. Customer Service Agent
customer_service_agent = Agent(
    role="Customer Service Representative",
    prompt_persona="""You are a friendly and helpful customer service representative.
    You handle general inquiries, account questions, and provide basic information.
    If you encounter technical issues, you should suggest: 'HANDOFF: technical_support'.
    If you encounter sales/pricing questions, you should suggest: 'HANDOFF: sales'."""
)

# 2. Technical Support Agent
technical_support_agent = Agent(
    role="Technical Support Specialist",
    prompt_persona="""You are an expert technical support specialist.
    You troubleshoot technical issues, provide detailed technical guidance, and solve complex problems.
    You have deep knowledge of system architecture, APIs, and debugging.
    If the issue is not technical, suggest: 'HANDOFF: customer_service'."""
)

# 3. Sales Agent
sales_agent = Agent(
    role="Sales Representative",
    prompt_persona="""You are an experienced sales representative.
    You handle product inquiries, pricing questions, feature comparisons, and help with purchasing decisions.
    You are persuasive but honest. If questions are not sales-related, suggest: 'HANDOFF: customer_service'."""
)

# Configure agents with their capabilities
agent_configs = [
    AgentConfig(
        agent=customer_service_agent,
        agent_id="customer_service",
        capabilities="Handles general inquiries, account questions, basic support, greetings, and routing to specialists"
    ),
    AgentConfig(
        agent=technical_support_agent,
        agent_id="technical_support",
        capabilities="Handles technical issues, debugging, API problems, system errors, and technical troubleshooting"
    ),
    AgentConfig(
        agent=sales_agent,
        agent_id="sales",
        capabilities="Handles product inquiries, pricing questions, feature requests, upgrades, and purchasing decisions"
    ),
]

# Create the handoff pipeline
pipeline = HandoffPipeline(
    name="Customer Support System",
    router_model=router_model,
    agent_configs=agent_configs,
    default_agent_id="customer_service",  # Start with customer service
    max_handoffs=5,  # Prevent infinite loops
    enable_auto_routing=True,  # Enable automatic routing
)

# Example 1: General inquiry (should stay with customer service)
print("="*80)
print("EXAMPLE 1: General Inquiry")
print("="*80)
result1 = pipeline.run(
    initial_request="Hello, I'd like to know more about your company.",
    model=router_model,
)
print(f"\nFinal Response: {result1['final_response']}")
print(f"Total Handoffs: {result1['total_handoffs']}")
print()

# Example 2: Technical issue (should route to technical support)
print("="*80)
print("EXAMPLE 2: Technical Issue")
print("="*80)
result2 = pipeline.run(
    initial_request="I'm getting a 500 error when calling your API endpoint /api/users. Can you help?",
    model=router_model,
)
print(f"\nFinal Response: {result2['final_response']}")
print(f"Total Handoffs: {result2['total_handoffs']}")
print(f"Handoff History: {result2['handoff_history']}")
print()

# Example 3: Sales inquiry (should route to sales)
print("="*80)
print("EXAMPLE 3: Sales Inquiry")
print("="*80)
result3 = pipeline.run(
    initial_request="What's the pricing for your enterprise plan? I need it for a team of 50 people.",
    model=router_model,
)
print(f"\nFinal Response: {result3['final_response']}")
print(f"Total Handoffs: {result3['total_handoffs']}")
print()

# Example 4: Manual routing to specific agent
print("="*80)
print("EXAMPLE 4: Manual Routing")
print("="*80)
response = pipeline.run_with_agent(
    agent_id="technical_support",
    request="Explain how to optimize database queries in our system.",
    model=router_model,
)
print(f"\nResponse: {response}")
print()

# Show conversation history
print("="*80)
print("CONVERSATION HISTORY")
print("="*80)
print(pipeline.context.get_conversation_summary())
