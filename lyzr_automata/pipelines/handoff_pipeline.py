import time
from typing import Dict, List, Optional, Any
from lyzr_automata.agents.agent_base import Agent
from lyzr_automata.ai_models.model_base import AIModel
from lyzr_automata.logger import Logger
from lyzr_automata.tasks.task_base import Task
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.utils.resource_handler import ResourceBox


class AgentConfig:
    """Configuration for an agent in the handoff pipeline."""

    def __init__(
        self,
        agent: Agent,
        capabilities: str,
        agent_id: str = None,
    ):
        """
        Initialize an agent configuration.

        Args:
            agent: The Agent instance
            capabilities: Description of what this agent can do
            agent_id: Unique identifier for the agent (defaults to agent.role)
        """
        self.agent = agent
        self.capabilities = capabilities
        self.agent_id = agent_id or agent.role


class ConversationContext:
    """Manages conversation history and context across agent handoffs."""

    def __init__(self):
        self.messages: List[Dict[str, Any]] = []
        self.handoff_history: List[Dict[str, Any]] = []
        self.current_agent_id: Optional[str] = None

    def add_message(self, role: str, content: str, agent_id: str = None):
        """Add a message to the conversation history."""
        message = {
            "role": role,
            "content": content,
            "timestamp": time.time(),
        }
        if agent_id:
            message["agent_id"] = agent_id
        self.messages.append(message)

    def add_handoff(self, from_agent: str, to_agent: str, reason: str = ""):
        """Record an agent handoff."""
        self.handoff_history.append({
            "from": from_agent,
            "to": to_agent,
            "reason": reason,
            "timestamp": time.time(),
        })
        self.current_agent_id = to_agent

    def get_conversation_summary(self) -> str:
        """Get a formatted summary of the conversation."""
        summary = []
        for msg in self.messages:
            agent_info = f" [{msg.get('agent_id', 'user')}]" if 'agent_id' in msg else ""
            summary.append(f"{msg['role']}{agent_info}: {msg['content']}")
        return "\n".join(summary)


class HandoffPipeline:
    """
    Pipeline that enables dynamic agent handoffs based on request context.

    Agents can automatically hand off tasks to other agents based on their
    capabilities and the nature of the request.
    """

    def __init__(
        self,
        name: str,
        router_model: AIModel,
        agent_configs: List[AgentConfig],
        default_agent_id: str = None,
        max_handoffs: int = 10,
        logger: Logger = None,
        resource_box: ResourceBox = ResourceBox(base_folder="resources"),
        enable_auto_routing: bool = True,
    ):
        """
        Initialize the handoff pipeline.

        Args:
            name: Pipeline name
            router_model: AI model used for routing decisions
            agent_configs: List of agent configurations
            default_agent_id: ID of the default agent to start with
            max_handoffs: Maximum number of handoffs to prevent infinite loops
            logger: Logger instance for tracking
            resource_box: Resource management
            enable_auto_routing: Whether to automatically route based on LLM decisions
        """
        self.name = name
        self.router_model = router_model
        self.agent_configs = {config.agent_id: config for config in agent_configs}
        self.default_agent_id = default_agent_id or agent_configs[0].agent_id
        self.max_handoffs = max_handoffs
        self.logger = logger
        self.resource_box = resource_box
        self.enable_auto_routing = enable_auto_routing
        self.context = ConversationContext()

        if not self.agent_configs:
            raise ValueError("At least one agent configuration is required")

    def _get_router_prompt(self, user_request: str) -> str:
        """Generate the routing prompt for agent selection."""
        agent_descriptions = []
        for agent_id, config in self.agent_configs.items():
            agent_descriptions.append(
                f"- {agent_id}: {config.capabilities}"
            )

        agents_info = "\n".join(agent_descriptions)
        conversation_history = self.context.get_conversation_summary()

        prompt = f"""You are an intelligent agent router. Based on the user's request and conversation history, determine which agent should handle this request.

Available Agents:
{agents_info}

Conversation History:
{conversation_history}

Current Request: {user_request}

Instructions:
1. Analyze the user's request carefully
2. Consider the conversation history and context
3. Select the most appropriate agent based on their capabilities
4. If the request requires the current agent, you can keep it
5. Respond with ONLY the agent ID (e.g., "{list(self.agent_configs.keys())[0]}")

Selected Agent:"""
        return prompt

    def _route_to_agent(self, user_request: str, current_agent_id: str = None) -> str:
        """
        Determine which agent should handle the request.

        Args:
            user_request: The user's request
            current_agent_id: Currently active agent ID

        Returns:
            Selected agent ID
        """
        if not self.enable_auto_routing:
            return current_agent_id or self.default_agent_id

        routing_prompt = self._get_router_prompt(user_request)

        response = self.router_model.generate_text(
            system_persona="You are an expert agent router that selects the best agent for each task.",
            prompt=routing_prompt,
        )

        # Extract agent ID from response
        selected_agent_id = response.strip().split()[0]

        # Validate the selected agent exists
        if selected_agent_id not in self.agent_configs:
            print(f"Warning: Router selected invalid agent '{selected_agent_id}', using default")
            selected_agent_id = self.default_agent_id

        return selected_agent_id

    def _execute_with_agent(
        self,
        agent_config: AgentConfig,
        user_request: str,
        model: AIModel = None,
        output_type: OutputType = OutputType.TEXT,
    ) -> str:
        """
        Execute a task with the specified agent.

        Args:
            agent_config: Configuration of the agent to use
            user_request: The user's request
            model: AI model to use (defaults to router_model)
            output_type: Type of output expected

        Returns:
            Agent's response
        """
        task_model = model or self.router_model

        # Create a task for this agent
        task = Task(
            name=f"{agent_config.agent_id}_task",
            agent=agent_config.agent,
            model=task_model,
            instructions=user_request,
            output_type=output_type,
            input_type=InputType.TEXT,
            default_input=self.context.get_conversation_summary(),
            resource_box=self.resource_box,
            logger=self.logger,
        )

        # Execute the task
        result = task.execute()
        return str(result)

    def _check_for_handoff_request(self, response: str) -> Optional[str]:
        """
        Check if the agent's response indicates a handoff is needed.

        Args:
            response: Agent's response

        Returns:
            Agent ID to hand off to, or None
        """
        # Check for explicit handoff markers
        handoff_markers = ["HANDOFF:", "TRANSFER:", "ROUTE_TO:"]
        for marker in handoff_markers:
            if marker in response.upper():
                # Extract the target agent from the response
                parts = response.upper().split(marker)
                if len(parts) > 1:
                    target = parts[1].strip().split()[0]
                    if target in self.agent_configs:
                        return target
        return None

    def run(
        self,
        initial_request: str,
        model: AIModel = None,
        output_type: OutputType = OutputType.TEXT,
    ) -> Dict[str, Any]:
        """
        Run the handoff pipeline with automatic agent routing.

        Args:
            initial_request: The initial user request
            model: AI model to use for tasks (defaults to router_model)
            output_type: Expected output type

        Returns:
            Dictionary containing final response and execution metadata
        """
        execution_start_time = time.time()
        print(f"START HANDOFF PIPELINE {self.name} :: start time: {execution_start_time}")

        # Add initial request to context
        self.context.add_message("user", initial_request)

        current_request = initial_request
        current_agent_id = self.default_agent_id
        handoff_count = 0
        responses = []

        while handoff_count < self.max_handoffs:
            # Route to appropriate agent
            selected_agent_id = self._route_to_agent(current_request, current_agent_id)

            # Record handoff if agent changed
            if selected_agent_id != current_agent_id:
                reason = f"Routing request to {selected_agent_id}"
                self.context.add_handoff(
                    from_agent=current_agent_id or "system",
                    to_agent=selected_agent_id,
                    reason=reason
                )
                print(f"HANDOFF: {current_agent_id or 'system'} -> {selected_agent_id}")
                handoff_count += 1
                current_agent_id = selected_agent_id

            # Execute with selected agent
            agent_config = self.agent_configs[selected_agent_id]
            print(f"EXECUTING with agent: {selected_agent_id}")

            response = self._execute_with_agent(
                agent_config=agent_config,
                user_request=current_request,
                model=model,
                output_type=output_type,
            )

            # Add response to context
            self.context.add_message("assistant", response, agent_id=selected_agent_id)
            responses.append({
                "agent_id": selected_agent_id,
                "response": response,
            })

            # Check if agent is requesting a handoff
            handoff_target = self._check_for_handoff_request(response)
            if handoff_target:
                print(f"Agent {selected_agent_id} requested handoff to {handoff_target}")
                current_agent_id = handoff_target
                handoff_count += 1
                continue

            # If no handoff needed, we're done
            break

        execution_end_time = time.time()
        execution_time = execution_end_time - execution_start_time

        print(f"END HANDOFF PIPELINE {self.name} :: end time: {execution_end_time} :: execution time: {execution_time}")
        print(f"Total handoffs: {handoff_count}")

        return {
            "final_response": responses[-1]["response"] if responses else "",
            "all_responses": responses,
            "handoff_history": self.context.handoff_history,
            "conversation_history": self.context.messages,
            "execution_time": execution_time,
            "total_handoffs": handoff_count,
        }

    def run_with_agent(
        self,
        agent_id: str,
        request: str,
        model: AIModel = None,
        output_type: OutputType = OutputType.TEXT,
    ) -> str:
        """
        Run a request with a specific agent (manual routing).

        Args:
            agent_id: ID of the agent to use
            request: The request to process
            model: AI model to use
            output_type: Expected output type

        Returns:
            Agent's response
        """
        if agent_id not in self.agent_configs:
            raise ValueError(f"Agent '{agent_id}' not found in pipeline")

        agent_config = self.agent_configs[agent_id]

        # Add to context
        self.context.add_message("user", request)
        if self.context.current_agent_id and self.context.current_agent_id != agent_id:
            self.context.add_handoff(
                from_agent=self.context.current_agent_id,
                to_agent=agent_id,
                reason="Manual routing"
            )
        self.context.current_agent_id = agent_id

        response = self._execute_with_agent(
            agent_config=agent_config,
            user_request=request,
            model=model,
            output_type=output_type,
        )

        self.context.add_message("assistant", response, agent_id=agent_id)
        return response
