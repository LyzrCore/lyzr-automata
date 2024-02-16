from abc import ABC, abstractmethod


class AIModel(ABC):
    @abstractmethod
    def generate_text(self, task_id, system_persona, prompt,tasks):
        pass

    @abstractmethod
    def generate_image(self, task_id, prompt, resource_box,tasks):
        pass