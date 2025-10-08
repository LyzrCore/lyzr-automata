# HandoffPipeline - Agentic Handoff Orchestration

## Overview

The `HandoffPipeline` is a new orchestration mechanism in Lyzr Automata that enables dynamic agent-to-agent handoffs based on request context. This allows you to build sophisticated multi-agent systems where specialized agents collaborate to handle complex workflows.

## Key Features

- **Automatic Routing**: LLM-powered agent selection based on request context
- **Manual Routing**: Explicit control over which agent handles each request
- **Conversation Context**: Full conversation history maintained across handoffs
- **Handoff Tracking**: Complete audit trail of all agent handoffs
- **Flexible Configuration**: Easy setup with agent capabilities and specializations
- **Loop Prevention**: Configurable maximum handoffs to prevent infinite loops

## Architecture

### Core Components

1. **HandoffPipeline**: Main orchestration class that manages agent routing and execution
2. **AgentConfig**: Configuration wrapper for agents with their capabilities
3. **ConversationContext**: Manages conversation history and handoff tracking

### How It Works

```
User Request → Router → Agent Selection → Task Execution → Response
                ↑                                          ↓
                └──────── Check for Handoff ──────────────┘
```

## Basic Usage

### 1. Import Required Classes

```python
from lyzr_automata import Agent, HandoffPipeline, AgentConfig
from lyzr_automata.ai_models.openai import OpenAIModel
```

### 2. Create Specialized Agents

```python
customer_service = Agent(
    role="Customer Service Rep",
    prompt_persona="You handle general inquiries and route complex issues to specialists."
)

technical_support = Agent(
    role="Technical Support",
    prompt_persona="You handle technical issues and troubleshooting."
)
```

### 3. Configure Agents with Capabilities

```python
agent_configs = [
    AgentConfig(
        agent=customer_service,
        agent_id="customer_service",
        capabilities="General inquiries, account questions, basic support"
    ),
    AgentConfig(
        agent=technical_support,
        agent_id="technical_support",
        capabilities="Technical issues, debugging, system errors"
    ),
]
```

### 4. Create and Run Pipeline

```python
pipeline = HandoffPipeline(
    name="Support System",
    router_model=model,
    agent_configs=agent_configs,
    default_agent_id="customer_service",
    enable_auto_routing=True,
)

result = pipeline.run(
    initial_request="I'm getting API errors",
    model=model,
)

print(result['final_response'])
print(f"Handoffs: {result['total_handoffs']}")
```

## Advanced Features

### Automatic Routing

The pipeline uses an LLM to automatically select the best agent for each request:

```python
pipeline = HandoffPipeline(
    name="Auto-Router",
    router_model=model,
    agent_configs=agent_configs,
    enable_auto_routing=True,  # Enables automatic routing
)
```

### Manual Routing

You can explicitly route to specific agents:

```python
response = pipeline.run_with_agent(
    agent_id="technical_support",
    request="Explain database optimization",
    model=model,
)
```

### Explicit Handoff Requests

Agents can request handoffs by including markers in their responses:

```python
agent = Agent(
    role="Receptionist",
    prompt_persona="""If you encounter technical issues, say:
    'HANDOFF: technical_support' to transfer to tech support."""
)
```

Supported markers:
- `HANDOFF: agent_id`
- `TRANSFER: agent_id`
- `ROUTE_TO: agent_id`

### Conversation Context

Access full conversation history:

```python
# Get formatted conversation summary
summary = pipeline.context.get_conversation_summary()

# Access all messages
for msg in pipeline.context.messages:
    print(f"{msg['role']}: {msg['content']}")

# Access handoff history
for handoff in pipeline.context.handoff_history:
    print(f"{handoff['from']} -> {handoff['to']}")
```

## Configuration Options

### HandoffPipeline Parameters

| Parameter | Type | Description | Default |
|-----------|------|-------------|---------|
| `name` | str | Pipeline name | Required |
| `router_model` | AIModel | Model for routing decisions | Required |
| `agent_configs` | List[AgentConfig] | Agent configurations | Required |
| `default_agent_id` | str | Starting agent | First agent |
| `max_handoffs` | int | Maximum handoffs allowed | 10 |
| `enable_auto_routing` | bool | Enable automatic routing | True |
| `logger` | Logger | Logger instance | None |
| `resource_box` | ResourceBox | Resource management | Default |

### AgentConfig Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `agent` | Agent | The agent instance |
| `capabilities` | str | Description of agent's capabilities |
| `agent_id` | str | Unique identifier (defaults to agent.role) |

## Return Values

The `run()` method returns a dictionary with:

```python
{
    "final_response": str,              # Final agent response
    "all_responses": List[dict],        # All responses from all agents
    "handoff_history": List[dict],      # Record of all handoffs
    "conversation_history": List[dict], # Full conversation
    "execution_time": float,            # Total execution time
    "total_handoffs": int,              # Number of handoffs performed
}
```

## Use Cases

### 1. Customer Support Systems
Route customers to specialized agents based on their inquiry type.

### 2. Content Creation Workflows
Coordinate multiple agents (researcher, writer, editor, SEO) in a pipeline.

### 3. Multi-Domain Assistants
Build assistants that handle diverse topics by routing to domain experts.

### 4. Complex Business Processes
Orchestrate workflows with multiple approval stages or specialist reviews.

### 5. Interactive Applications
Create conversational apps where different agents handle different conversation stages.

## Examples

See the example files:
- `handoff_example.py` - Basic customer support system
- `content_creation_handoff.py` - Complex content creation workflow

## Best Practices

1. **Clear Agent Capabilities**: Define specific, non-overlapping capabilities for better routing
2. **Reasonable Max Handoffs**: Set appropriate limits to prevent infinite loops
3. **Explicit Handoff Instructions**: Train agents when to request handoffs
4. **Monitor Handoff Patterns**: Review handoff history to optimize agent design
5. **Use Manual Routing for Deterministic Flows**: Disable auto-routing for predictable workflows

## Comparison with LinearSyncPipeline

| Feature | LinearSyncPipeline | HandoffPipeline |
|---------|-------------------|-----------------|
| Execution Order | Fixed, sequential | Dynamic, context-based |
| Agent Selection | Predefined | Automatic or manual |
| Conversation Context | Task outputs only | Full conversation history |
| Routing Logic | None | LLM-powered or manual |
| Use Case | Predictable workflows | Adaptive, multi-agent systems |

## Troubleshooting

### Infinite Handoff Loops
**Problem**: Agents keep handing off back and forth.
**Solution**: Increase agent specialization clarity, adjust `max_handoffs`, or use manual routing.

### Incorrect Agent Selection
**Problem**: Router selects wrong agent.
**Solution**: Make agent capabilities more specific and distinct, or use manual routing.

### Loss of Context
**Problem**: Agents seem to forget previous conversation.
**Solution**: Ensure agents use `self.context.get_conversation_summary()` in their prompts.

## API Reference

### HandoffPipeline

#### `__init__(name, router_model, agent_configs, ...)`
Initialize the handoff pipeline.

#### `run(initial_request, model=None, output_type=OutputType.TEXT)`
Run the pipeline with automatic routing.

#### `run_with_agent(agent_id, request, model=None, output_type=OutputType.TEXT)`
Run with a specific agent (manual routing).

### ConversationContext

#### `add_message(role, content, agent_id=None)`
Add a message to conversation history.

#### `add_handoff(from_agent, to_agent, reason="")`
Record an agent handoff.

#### `get_conversation_summary()`
Get formatted conversation summary.

## Contributing

To extend the HandoffPipeline:
1. Add custom routing logic by subclassing `HandoffPipeline`
2. Implement custom `_route_to_agent()` method
3. Add new handoff markers in `_check_for_handoff_request()`

## License

Same as Lyzr Automata (MIT License)
