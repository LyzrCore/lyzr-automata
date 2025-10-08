# Quick Start: HandoffPipeline

## 5-Minute Setup

### 1. Install Lyzr Automata
```bash
pip install lyzr-automata
```

### 2. Basic Example (10 lines)

```python
from lyzr_automata import Agent, HandoffPipeline, AgentConfig
from lyzr_automata.ai_models.openai import OpenAIModel

# Create model
model = OpenAIModel(api_key="your-key", parameters={"model": "gpt-4"})

# Create agents
support = Agent(role="Support", prompt_persona="General support agent")
tech = Agent(role="Tech", prompt_persona="Technical specialist")

# Configure with capabilities
configs = [
    AgentConfig(support, "support", "General inquiries"),
    AgentConfig(tech, "tech", "Technical issues")
]

# Create pipeline
pipeline = HandoffPipeline("System", model, configs)

# Run with automatic routing
result = pipeline.run("API is returning 500 errors", model=model)
print(result['final_response'])
```

### 3. Key Concepts

**Agent** → Has a role and persona
**AgentConfig** → Defines what an agent can do
**HandoffPipeline** → Routes requests to the right agent

### 4. Routing Types

**Automatic** (default)
```python
# LLM decides which agent to use
result = pipeline.run("Your request here")
```

**Manual**
```python
# You decide which agent to use
result = pipeline.run_with_agent("tech", "Your request")
```

### 5. Get Results

```python
result = pipeline.run("request")

print(result['final_response'])     # Final answer
print(result['total_handoffs'])     # Number of agent switches
print(result['handoff_history'])    # Who handed off to whom
```

## Common Patterns

### Customer Support
```python
agents = [
    AgentConfig(billing_agent, "billing", "Billing and payments"),
    AgentConfig(tech_agent, "tech", "Technical support"),
    AgentConfig(sales_agent, "sales", "Product and pricing")
]
```

### Content Pipeline
```python
agents = [
    AgentConfig(researcher, "research", "Gather information"),
    AgentConfig(writer, "write", "Create content"),
    AgentConfig(editor, "edit", "Review and improve")
]
```

### Business Workflow
```python
agents = [
    AgentConfig(analyst, "analyze", "Data analysis"),
    AgentConfig(reviewer, "review", "Quality review"),
    AgentConfig(approver, "approve", "Final approval")
]
```

## Handoff Triggers

Agents can trigger handoffs:

```python
agent = Agent(
    role="Receptionist",
    prompt_persona="If technical issue, say 'HANDOFF: tech'"
)
```

Keywords: `HANDOFF:`, `TRANSFER:`, `ROUTE_TO:`

## Need More?

- Full Documentation: `examples/HANDOFF_README.md`
- Basic Example: `examples/handoff_example.py`
- Advanced Example: `examples/content_creation_handoff.py`
- Test Script: `examples/handoff_test_simple.py`

## Tips

1. **Clear capabilities** → Better routing
2. **Set max_handoffs** → Prevent loops (default: 10)
3. **Use manual routing** → For predictable flows
4. **Check handoff_history** → Debug routing issues

---

That's it! You now have intelligent agent handoffs. 🚀
