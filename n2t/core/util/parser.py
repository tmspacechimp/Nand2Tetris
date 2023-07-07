import re
from typing import Iterable, Protocol

from n2t.core.util.trash_filter import SpacesLineFilter


class InstructionParser(Protocol):
    @classmethod
    def __call__(cls, instruction_str: str) -> str:
        pass


class IJackSplitter(Protocol):
    @classmethod
    def __call__(cls, jack_str: str) -> Iterable[str]:
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


class JackSplitter(IJackSplitter):
    @classmethod
    def split(cls, jack_str: str) -> Iterable[str]:
        return list(
            filter(
                SpacesLineFilter.passes,
                re.split(r"(\s+|\(|\)|\.|\[|\]|\;|\,)", jack_str),
            )
        )

    @classmethod
    def __call__(cls, jack_str: str) -> Iterable[str]:
        return cls.split(jack_str)
