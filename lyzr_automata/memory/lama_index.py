from typing import Any, Dict, List
from fastapi.responses import FileResponse

import openai
from lyzr_automata.ai_models.model_base import AIModel
from lyzr_automata.memory.memory_literals import MemoryProvider
import os

from lyzr_automata.utils.resource_handler import ResourceBox


class LlamaMemoryModel(AIModel):
    def __init__(self, api_key, parameters: Dict[str, Any]):
        self.parameters = parameters
        os.environ["OPENAI_API_KEY"] = api_key
        self.llama_index = parameters["index"]
        self.query_engine = self.llama_index.as_query_engine()

    def generate_text(
        self,
        task_id: str = None,
        system_persona: str = None,
        prompt: str = None,
        messages: List[dict] = None,
    ):
        response = self.query_engine.query(f"{system_persona} {prompt}")
        return response
    
    def generate_image(
        self, task_id: str, prompt: str, resource_box: ResourceBox
    ) -> FileResponse:
        # kept empty because model doesn't support image generation
        pass


class LlamaMemory:
    memory_type = MemoryProvider.LLAMA_INDEX

    def __init__(self, llama_index):
        self.llama_index = llama_index

    def generate_memory_model(self, model: AIModel):
        return LlamaMemoryModel(
            api_key=model.api_key,
            parameters={"index": self.llama_index, **model.parameters},
        )
