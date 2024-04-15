from typing import Any, Dict, List
from groq import Groq
from lyzr_automata.ai_models.model_base import AIModel
from lyzr_automata.data_models import FileResponse
from lyzr_automata.utils.resource_handler import ResourceBox
import groq


class GroqModel(AIModel):
    def __init__(self, api_key, parameters: Dict[str, Any]):
        self.parameters = parameters
        self.client = Groq(api_key=api_key)
        self.api_key = api_key

    def generate_text(
        self,
        task_id: str=None,
        system_persona: str=None,
        prompt: str=None,
        messages: List[dict] = None,
    ):
        if messages is None:
            messages = [
                {"role": "system", "content": system_persona},
                {"role": "user", "content": prompt},
            ]

        try:
            response = self.client.chat.completions.create(
                **self.parameters,
                messages=messages
            )

            return response.choices[0].message.content
        except groq.APIConnectionError as e:
            print("The server could not be reached")
            print(e.__cause__)
        except (groq.RateLimitError, groq.APIStatusError) as e:
            print("An error occurred while making the request")
            print(type(e))
            print(e)

    def generate_image(
        self, task_id: str, prompt: str, resource_box: ResourceBox
    ) -> FileResponse:
        pass