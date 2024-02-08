from typing import Dict, List
from typing import Any

import requests

from lyzr_automata.ai_models.model_base import AIModel
from lyzr_automata.data_models import FileResponse
from lyzr_automata.utils.resource_handler import ResourceBox


class PerplexityModel(AIModel):
    def __init__(self, api_key, parameters: Dict[str, Any]):
        self.parameters = parameters
        self.api_key = api_key

    def query_perplexity_api(
        self,
        messages,
    ):
        # API endpoint
        url = "https://api.perplexity.ai/chat/completions"

        # Headers for the request
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.api_key}",
            "content-type": "application/json",
        }

        # Data payload for the request, including system and user messages
        data = {**self.parameters, "messages": messages}

        # Sending POST request to the API
        response = requests.post(url, headers=headers, json=data)

        # Return the API response
        if response.status_code == 200:
            return response.json()
        else:
            return response.text

    def generate_text(
        self,
        task_id: str = None,
        system_persona: str = "You are a search engine. Execute the search for the phrase provided by the user. provide only the search results of the output. Do not share the steps or the methods that we used to generate the results",
        prompt: str = None,
        messages: List[Dict] = None,
    ):
        # task_id kept for future use
        if messages is None:
            messages = [
                {"role": "system", "content": system_persona},
                {"role": "user", "content": prompt},
            ]

        response = self.query_perplexity_api(messages)
        return response

    def generate_image(
        self, task_id: str, prompt: str, resource_box: ResourceBox
    ) -> FileResponse:
        # kept empty because model doesn't support image generation
        pass
