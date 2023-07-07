from dataclasses import dataclass
from typing import Dict, Protocol


@dataclass
class ComponentInfo:
    scope: str  # maybe not the best name, meaning static or this e.g.
    type: str
    index: int


class INameSpace(Protocol):
    def define(self, name: str, scope: str, of_type: str) -> int:
        pass

    def is_defined(self, name: str) -> bool:
        pass

    def get(self, name: str) -> ComponentInfo:
        pass

    def count(self, scope: str) -> int:
        pass

    def init_sub(self) -> None:
        pass


class NameSpace(INameSpace):
    class_space: Dict[str, ComponentInfo] = {}
    subroutine_space: Dict[str, ComponentInfo] = {}
    next_indexes: Dict[str, int] = {"this": 0, "static": 0, "local": 0, "argument": 0}

    def define(self, name: str, scope: str, of_type: str) -> int:
        if scope in ["field", "static"]:
            scope = scope if scope == "static" else "this"
            index = self.count(scope)
            self.class_space[name] = ComponentInfo(scope, of_type, index)
        else:
            index = self.count(scope)
            self.subroutine_space[name] = ComponentInfo(scope, of_type, index)

        self.next_indexes[scope] += 1
        return index

    def is_defined(self, name: str) -> bool:
        return name in self.class_space or name in self.subroutine_space

    def get(self, name: str) -> ComponentInfo:
        if not self.is_defined(name):
            print(name)
            print(self.subroutine_space)
            raise KeyError
        if name in self.class_space:
            return self.class_space[name]
        return self.subroutine_space[name]

    def count(self, scope: str) -> int:
        return self.next_indexes[scope]

    def init_sub(self) -> None:
        self.subroutine_space = {}
        self.next_indexes["local"] = 0
        self.next_indexes["argument"] = 0
