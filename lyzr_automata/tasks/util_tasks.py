from lyzr_automata.ai_models.model_base import AIModel
from lyzr_automata.tasks.task_literals import InputType, OutputType
from lyzr_automata.tasks.task_base import Task


def summarize_task(words_length: int, text_ai_model: AIModel) -> Task:
    return Task(
        output_type=OutputType.TEXT,
        input_type=InputType.TEXT,
        model=text_ai_model,
        instructions=f"summarize the given input to exactly {words_length} words strictly and send the response",
    )