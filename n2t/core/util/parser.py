from typing import Protocol


class InstructionParser(Protocol):
    @classmethod
    def __call__(cls, instruction_str: str) -> str:
        pass


class DeleteCommentAndStrip(InstructionParser):
    @classmethod
    def parse(cls, instruction_string: str) -> str:
        index = instruction_string.find("//")
        if index != -1:
            instruction_string = instruction_string[:index]
        return instruction_string.strip()

    @classmethod
    def __call__(cls, instruction_str: str) -> str:
        return cls.parse(instruction_str)
