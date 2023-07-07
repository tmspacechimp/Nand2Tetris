from dataclasses import dataclass, field
from re import match
from typing import Protocol, Tuple


class TrashFilter(Protocol):
    @classmethod
    def passes(cls, instruction_str: str) -> bool:
        pass


class CommentFilter(TrashFilter):
    @classmethod
    def passes(cls, instruction_str: str) -> bool:
        return not (
            instruction_str.startswith("//")
            or match(r"^\s*//", instruction_str)
            or match(r"^\s*/\*\*", instruction_str)
            or match(r"^\s*\*", instruction_str)
            or match(r"^\s*\*/", instruction_str)
        )


class EmptyLineFilter(TrashFilter):
    @classmethod
    def passes(cls, instruction_str: str) -> bool:
        return not (instruction_str == "")


class SpacesLineFilter(TrashFilter):
    @classmethod
    def passes(cls, instruction_str: str) -> bool:
        return not match(r"^\s*$", instruction_str)


@dataclass
class CompositeTrashFilter(TrashFilter):
    filters: Tuple[TrashFilter, ...] = field(
        default=(EmptyLineFilter(), CommentFilter())
    )

    @classmethod
    def passes(cls, instruction_str: str) -> bool:
        for f in cls.filters:
            if not f.passes(instruction_str):
                return False
        return True
