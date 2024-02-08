from lyzr_automata.tools.linkedin import LinkedInPostInput, LinkedInPostOutput, post_image_and_text
from lyzr_automata.tools.tool_base import Tool


def linkedin_image_text_post_tool(owner:str,token:str):
    return Tool(
    name="LinkedIn Post",
    desc="Posts an post on linkedin provided details.",
    function=post_image_and_text,
    function_input=LinkedInPostInput,
    function_output=LinkedInPostOutput,
    default_params= {
        "owner":owner,
        "token":token
    }
)