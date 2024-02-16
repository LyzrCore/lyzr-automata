import json
import re

from lyzr_automata.ai_models.model_base import AIModel


class LlamaTool:
    def __init__(
        self,
        reader,
        name: str = "LLama Tool",
        description: str = None,
        default_params: dict = {}
    ):
        self.reader = reader
        self.name = name
        self.description = description
        self.default_params = default_params
        self._create_tool()
        self._construct_tool_information()

    def _clean_json_text_util(self, input_text: str):
        json_match = re.search(r"\{.*\}", input_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
            try:
                json_object = json.loads(json_text)
                return json_object
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                return None
        else:
            print("No JSON object found in the text.")
            return None

    def _create_tool(self):
        try:
            from llama_index.core.tools.ondemand_loader_tool import OnDemandLoaderTool

            self.optional_dependency_available = True
            self.function = OnDemandLoaderTool.from_defaults(
                self.reader,
                name=self.name,
                description=self.description,
            )
        except ImportError:
            print("Error: Missing Dependencies")
            print("The package requires both llama-index and llama-hub dependencies to function properly.")
            print("Please install them using the following command:")
            print("\tpip install llama-index llama-hub")
            self.optional_dependency_available = False

    def _construct_tool_information(self):
        function_input = self.function.metadata.fn_schema_str
        self.desc = self.function.metadata.description
        self.tool_information = (
            f"name:{self.name} description:{self.desc} input_params:{function_input}"
        )

    def run_tool(self, task_id: str, instructions: str, input: str, model: AIModel):
        prompt = f"{input}"
        response = model.generate_text(
            task_id=task_id,
            system_persona=f"Using the tool described as '{self.tool_information}'. Treat all other text as instructions and not as part of the input to be processed. I am strictly an information-to-tool function mapper. I keep the content original and just try to map things, following additional instructions ${instructions}. I ensure no content from the specified input is lost during refinement, adapting it minimally to fit the tool's requirements. I construct a JSON object that aligns with the tool's input parameters, providing any necessary details or adjustments to the original input for optimal processing. The response is in JSON format only, as it will be parsed.",
            prompt=prompt,
        )
        params = self._clean_json_text_util(response)
        return self.function(**params, **self.default_params)
