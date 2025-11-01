from __future__ import annotations
import time
from typing import Any, List, Union
import uuid
import re
from lyzr_automata.agents.agent_base import Agent
from lyzr_automata.ai_models.model_base import AIModel
from lyzr_automata.logger import Logger
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.tools.tool_base import Tool
from lyzr_automata.utils.prompt_utils import enhance_prompt
from lyzr_automata.utils.resource_handler import ResourceBox


class Task:
    def __init__(
        self,
        model: AIModel,
        instructions: str = "",
        default_input: str = "",
        name: str = None,
        log_output: bool = False,
        output_type: Union[OutputType, str] = OutputType.TEXT,
        agent: Agent = Agent(role="", prompt_persona=""),
        input_type: Union[InputType, str] = InputType.TEXT,
        tool: Tool = None,
        file_paths: List[str] = None,
        previous_output: Any = None,
        resource_box: ResourceBox = ResourceBox(),
        input_tasks: List[Task] = None,
        enhance_prompt: bool = False,
        logger: Logger = None,
        chunk_size: int = 4096,
    ):
        self.input_type = input_type
        self.instructions = instructions
        self.output_type = output_type
        self.file_paths = file_paths if file_paths is not None else []
        self.agent = agent
        self.tool = tool
        self.previous_output = previous_output
        self.resource_box = resource_box
        self.input_tasks = input_tasks
        self.log_output = log_output
        self.enhance_prompt = enhance_prompt
        self.default_input = str(default_input)
        self.task_id = uuid.uuid4()
        self.name = name
        self.logger = logger
        self.chunk_size = chunk_size
        if self.tool != None:
            self.output_type = OutputType.TOOL
        if self.name == None:
            self.name = self.task_id
        if self.input_tasks == None:
            self.input_tasks = []
        if self.agent.memory != None:
            self.model = self.agent.memory.generate_memory_model(model)
        else:
            self.model = model

        self._create_task_execution_method()

    def set_resource_box(self, resource_box: ResourceBox):
        self.resource_box = resource_box

    def _create_task_execution_method(self):
        system_persona = f"In your role as {self.agent.role}, you embody a persona defined by {self.agent.prompt_persona}."
        prompt = f"Now execute these instructions: {self.instructions}."

        # Determine execution method based on output type
        if self.output_type == OutputType.IMAGE:
            self._execute_task = lambda: self._generate_image(
                f"{system_persona} {prompt}"
            )
        if self.output_type == OutputType.TEXT:
            self._execute_task = lambda: self._generate_text(
                system_persona=system_persona, prompt=prompt
            )
        if self.output_type == OutputType.TOOL:
            self._execute_task = lambda: self._execute_tool(system_persona, prompt)

    def _generate_text(self, system_persona: str, prompt: str):
        if self.enhance_prompt:
            prompt = enhance_prompt(prompt=prompt, model=self.model)

        text_model_input = self.concatenate_strings(self.previous_output, self.default_input)
        text_model_input_list = self.chunk_by_sentences(text_model_input, self.chunk_size)

        generated_list = []
        for input_text in text_model_input_list:
            generated_output = self.model.generate_text(
                task_id=self.task_id,
                system_persona=system_persona,
                prompt=f"{prompt}  Input: {input_text}",
            )
            generated_list.append(generated_output)

        return generated_list

    def _generate_image(self, prompt: str):
        return self.model.generate_image(
            prompt=f"Create a image based on this prompt: {prompt} and Input: {self.previous_output} {self.default_input}. Dont include text in image",
            task_id=self.task_id,
            resource_box=self.resource_box,
        )

    def _execute_tool(self, system_persona, prompt):
        return self.tool.run_tool(
            instructions=f"${system_persona} ${prompt}",
            input=f"{self.previous_output} {self.default_input}",
            model=self.model,
            task_id=self.task_id,
        )

    def execute(self):
        if self.log_output == True:
            # TODO create a better logger
            execution_start_time = time.time()
            print(
                f"START TASK {self.name} :: start time : {str(execution_start_time)}"
            )
            self.output = self._execute_task()
            execution_end_time = time.time()
            execution_time = execution_end_time - execution_start_time
            print(f"output : {self.output}")
            print(
                f"END TASK {self.name} :: end time :  {str(execution_end_time)} :: execution time : {execution_time}"
            )
            if(self.logger is not None):
                self.logger.task(
                    start_time=execution_start_time,
                    end_time=execution_end_time,
                    execution_time=execution_time,
                    output=self.output,
                    name=self.name,
                )
        else:
            self.output = self._execute_task()
        return self.output
    
    def chunk_by_sentences(self, text, chunk_size):
        chunks = []
        current_chunk = ""
        for sentence in re.split(r'[.?!]+', text):
            if len(current_chunk + sentence) <= chunk_size:
                current_chunk += " " + sentence
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence
        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks
    
    def concatenate_strings(self, str1, str2):
        if str1 is None:
            str1 = ''
        if str2 is None:
            str2 = ''
        return str1 + str2