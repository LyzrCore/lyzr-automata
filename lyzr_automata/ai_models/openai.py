from typing import Any, Dict, List
from openai import OpenAI

from lyzr_automata.ai_models.model_base import AIModel
from lyzr_automata.data_models import FileResponse
from lyzr_automata.utils.resource_handler import ResourceBox


class OpenAIModel(AIModel):
    def __init__(self, api_key, parameters: Dict[str, Any]):
        self.parameters = parameters
        self.client = OpenAI(api_key=api_key)
        self.api_key = api_key

    def generate_text(
        self,
        task_id: str=None,
        system_persona: str=None,
        prompt: str=None,
        messages: List[dict] = None,
    ):
        # task_id kept for future use
        if messages is None:
            messages = [
                {"role": "system", "content": system_persona},
                {"role": "user", "content": prompt},
            ]

        response = self.client.chat.completions.create(
            **self.parameters, messages=messages
        )
        # TODO ability to return multiple responses
        return response.choices[0].message.content

    def generate_image(
        self, task_id: str, prompt: str, resource_box: ResourceBox
    ) -> FileResponse:
        response = self.client.images.generate(**self.parameters, prompt=prompt)
        return resource_box.save_from_url(url=response.data[0].url, subfolder=task_id)
