import json
import re

from lyzr_automata.ai_models.model_base import AIModel


class Tool:
    def __init__(
        self,
        name: str,
        desc: str,
        function: any,
        function_input: any,
        function_output: any,
        default_params: dict,
    ):
        self.name = name
        self.function = function
        self.desc = desc
        self.function_input = function_input
        self.function_output = function_output
        self.default_params = default_params
        if self.default_params == None:
            self.default_params = {}
        self._construct_tool_information()

    def _clean_json_text_util(self, input_text: str):
        # Use regular expression to find JSON object
        json_match = re.search(r"\{.*\}", input_text, re.DOTALL)
        if json_match:
            json_text = json_match.group(0)
            try:
                # Parse the JSON text to a Python dictionary
                json_object = json.loads(json_text)
                return json_object
            except json.JSONDecodeError as e:
                print(f"Error parsing JSON: {e}")
                return None
        else:
            print("No JSON object found in the text.")
            return None

    def _construct_tool_information(self):
        function_input = json.dumps(self.function_input.schema(), indent=2)
        function_output = json.dumps(self.function_output.schema(), indent=2)
        self.tool_information = f"name:{self.name} description:{self.desc} input_params:{function_input} output_model:{function_output}"

    def run_tool(self, task_id: str, instructions: str, input: str, model: AIModel):
        prompt = f"${input}"
        response = model.generate_text(
            task_id=task_id,
            system_persona=f"Using the tool described as '{self.tool_information}'. Treat all other text as instructions and not as part of the input to be processed. I am strictly an information-to-tool function mapper. I keep the content original and just try to map things, following additional instructions ${instructions}. I ensure no content from the specified input is lost during refinement, adapting it minimally to fit the tool's requirements. I construct a JSON object that aligns with the tool's input parameters, providing any necessary details or adjustments to the original input for optimal processing. The response is in JSON format only, as it will be parsed.",
            prompt=prompt,
        )
        params = self._clean_json_text_util(response)
        return self.function(**params,**self.default_params)