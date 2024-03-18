import json
import os
import time
from typing import Dict, Any, List, Optional

from fastapi.responses import FileResponse
from openai import OpenAI

from lyzr_automata.ai_models.model_base import AIModel
from lyzr_automata.memory.memory_literals import MemoryProvider
from lyzr_automata.utils.resource_handler import ResourceBox


class FileRetrievalAssistant:
    def __init__(
        self, persist: bool = True, ids_file: str = "assistant_ids.json"
    ) -> None:
        self.persist = persist
        self.ids_file = ids_file  # Path to the JSON file where IDs will be saved/loaded
        self.api_key: Optional[str] = os.getenv("OPENAI_API_KEY")
        if self.api_key is None:
            raise ValueError("API Key not found in environment variables")
        self.client = OpenAI(api_key=self.api_key)
        self.assistant_id: Optional[str] = None
        self.file_id: Optional[str] = None
        self.thread_id: Optional[str] = None
        if self.persist:
            self.load_ids_from_file()  # Attempt to load IDs from the file on initialization

    def upload_file(self, filename: str, model: str) -> None:
        if self.file_id is None:
            with open(filename, "rb") as f:
                file = self.client.files.create(file=f, purpose="assistants")
            self.file_id = file.id
            if self.persist:
                self.save_ids_to_file()  # Save IDs after creating the file

        if self.assistant_id is None:
            assistant = self.client.beta.assistants.create(
                name="File Helper",
                instructions="You are my assistant who can answer questions from the given file",
                tools=[{"type": "retrieval"}],
                model=model,
                file_ids=[self.file_id],
            )
            self.assistant_id = assistant.id
            if self.persist:
                self.save_ids_to_file()  # Save IDs after creating the assistant

    def save_ids_to_file(self) -> None:
        """Saves the current IDs to a JSON file."""
        ids = {
            "assistant_id": self.assistant_id,
            "file_id": self.file_id,
            "thread_id": self.thread_id,
        }
        with open(self.ids_file, "w") as file:
            json.dump(ids, file)

    def load_ids_from_file(self) -> None:
        """Loads the IDs from a JSON file, if it exists."""
        try:
            with open(self.ids_file, "r") as file:
                ids = json.load(file)
                self.assistant_id = ids.get("assistant_id")
                self.file_id = ids.get("file_id")
                # The thread_id is not loaded because a new thread is created for each session
        except FileNotFoundError:
            print("No existing IDs file found. Starting from scratch.")

    def get_answers(self, question: str) -> List[str]:
        if self.assistant_id is None:
            raise ValueError("Assistant not created. Please upload a file first.")

        thread = self.client.beta.threads.create()
        self.thread_id = thread.id

        self.client.beta.threads.messages.create(
            thread_id=self.thread_id, role="user", content=question
        )

        run = self.client.beta.threads.runs.create(
            thread_id=self.thread_id, assistant_id=self.assistant_id
        )

        while True:
            run_status = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread_id, run_id=run.id
            )
            if run_status.status == "completed":
                messages = self.client.beta.threads.messages.list(
                    thread_id=self.thread_id
                )
                break
            else:
                time.sleep(2)  # Adjust the sleep time as needed

        return [
            message.content for message in messages.data if message.role == "assistant"
        ]


class OpenAIFileMemoryModel(AIModel):
    def __init__(self, api_key, parameters: Dict[str, Any]):
        self.parameters = parameters
        os.environ["OPENAI_API_KEY"] = api_key
        self.model = self.parameters["model"]
        self.file_path = self.parameters["file_path"]
        self.persist = self.parameters["persist"]
        self.retriever = FileRetrievalAssistant(persist=True)
        self.retriever.upload_file(self.file_path, model=self.model)

    def generate_text(
        self,
        task_id: str = None,
        system_persona: str = None,
        prompt: str = None,
        messages: List[dict] = None,
    ):
        response =  self.retriever.get_answers(question=f"${system_persona} ${prompt}")
        return response

    def generate_image(
        self, task_id: str, prompt: str, resource_box: ResourceBox
    ) -> FileResponse:
        # kept empty because model doesn't support image generation
        pass


class OpenAIMemory:
    memory_type = MemoryProvider.OPEN_AI

    def __init__(
        self,
        file_path,
        persist = False,
    ):
        self.file_path = file_path
        self.persist = persist 

    def generate_memory_model(self, model: AIModel):
        return OpenAIFileMemoryModel(
            
            api_key=model.api_key,
            parameters={
                "file_path": self.file_path,
                "persist": self.persist,
                **model.parameters,
            },
        )
