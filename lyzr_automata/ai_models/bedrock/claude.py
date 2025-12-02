import boto3
import json
from botocore.exceptions import ClientError
from typing import Any, Dict, List

from lyzr_automata.ai_models.model_base import AIModel
from lyzr_automata.data_models import FileResponse
from lyzr_automata.utils.resource_handler import ResourceBox


class ClaudeModel(AIModel):
    def __init__(
        self,
        aws_access_key_id,
        aws_secret_access_key,
        region_name,
        model_id,
        parameters: Dict[str, Any],
    ):
        self.parameters = parameters
        # Initialize the Amazon Bedrock runtime client with AWS credentials
        self.client = boto3.client(
            service_name="bedrock-runtime",
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,  # API key assumed to be AWS access key
            aws_secret_access_key=aws_secret_access_key,  # AWS secret access key required
        )
        self.model_id = model_id  # Example model ID, adjust as necessary

    def generate_text(
        self,
        task_id: str = None,
        system_persona: str = None,
        prompt: str = None,
        messages: List[dict] = None,
    ):
        # Prepare the messages for the API request
        if messages is None:
            messages = [{"role": "user", "content": [{"type": "text", "text": prompt}]}]

        # The data payload for the POST request
        data_payload = {
            "messages": messages,
            **self.parameters,
        }

        if system_persona:
            data_payload["system"] = system_persona

        try:
            response = self.client.invoke_model(
                modelId=self.model_id,
                body=json.dumps(data_payload),
            )
            # Process and return the response
            result = json.loads(response["body"].read().decode('utf-8'))
            output_list = result.get("content", [])

            if output_list:
                return output_list[0]["text"]
            else:
                raise ValueError("No response content found.")

        except ClientError as err:
            raise Exception(
                f"Couldn't invoke Claude model. AWS error: {err.response['Error']['Code']}: {err.response['Error']['Message']}"
            )

    def generate_image(
        self, task_id: str, prompt: str, resource_box: ResourceBox
    ) -> FileResponse:
        # Kept empty for future use
        pass
