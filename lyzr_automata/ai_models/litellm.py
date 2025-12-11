from typing import Any, Dict, List, Optional
from litellm import completion
import os
import dotenv 
dotenv.load_dotenv()
from lyzr_automata.ai_models.model_base import AIModel
from lyzr_automata.data_models import FileResponse
from lyzr_automata.utils.resource_handler import ResourceBox


class LiteLLMModel(AIModel):
    def __init__(
        self,  model_name: str, parameters: Optional[Dict[str, Any]] = None
    ):
        self.model_name = model_name
        self.parameters = parameters or {}
    def generate_text(
        self,
        task_id: Optional[str] = None,
        system_persona: Optional[str] = None,
        prompt: Optional[str] = None,
        messages: Optional[List[Dict[str, str]]] = None,
    ) -> str:
        if messages is None:
            messages = [{"role": "user", "content": prompt}]

        if system_persona:
            messages.insert(0, {"role": "system", "content": system_persona})

        response = completion(
            model=self.model_name,
            messages=messages,
            **self.parameters,  # Pass additional parameters (e.g., temperature, max_tokens)
        )

        if response.choices and len(response.choices) > 0:
            return response.choices[0].message.content
        else:
            raise ValueError("No response content found.")

    def generate_image(
        self, task_id: str, prompt: str, resource_box: ResourceBox
    ) -> FileResponse:
        raise NotImplementedError("Image generation is not supported yet.")