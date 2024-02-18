class Agent:
    def __init__(self, role: str, memory=None,prompt_persona: str="") -> None:
        self.prompt_persona = prompt_persona
        self.role = role
        self.memory = memory