from dataclasses import dataclass, field
from re import match
from typing import Protocol, Tuple


class TrashFilter(Protocol):
    def passes(self, instruction_str: str) -> bool:
        pass


class CommentFilter(TrashFilter):
    def passes(self, instruction_str: str) -> bool:
        return not (
            instruction_str.startswith("//") or match(r"^\s*//", instruction_str)
        )


class EmptyLineFilter(TrashFilter):
    def passes(self, instruction_str: str) -> bool:
        return not (instruction_str == "")


@dataclass
class CompositeTrashFilter(TrashFilter):
    filters: Tuple[TrashFilter, ...] = field(
        default=(EmptyLineFilter(), CommentFilter())
    )

    def passes(self, instruction_str: str) -> bool:
        for f in self.filters:
            if not f.passes(instruction_str):
                return False
        return True
