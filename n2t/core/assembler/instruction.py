from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Dict, Protocol

from n2t.core.assembler.constants import COMP_TABLE, DEST_TABLE, JUMP_TABLE


@dataclass
class Instruction(ABC):
    assembly_str: str = field(init=True)
    addresses: Dict[str, int] = field(default_factory=dict)

    def set_addresses(self, addresses: Dict[str, int]) -> "Instruction":
        self.addresses = addresses
        return self

    @abstractmethod
    def get_bits(self) -> str:
        pass


@dataclass
class AInstruction(Instruction):
    def get_bits(self) -> str:
        content = self.assembly_str[1:]
        if content.isdecimal():
            address = int(content)
        else:
            address = self.addresses[content]
        return bin(address)[2:].zfill(16)


@dataclass
class CInstruction(Instruction):
    def __post_init__(self) -> None:
        self.equal_index = self.assembly_str.find("=")
        self.semicolon_index = self.assembly_str.find(";")

    def get_bits(self) -> str:
        return f"111{self.get_comp()}{self.get_dest()}{self.get_jump()}"

    def get_dest(self) -> str:
        if self.equal_index != -1:
            return DEST_TABLE[self.assembly_str[: self.equal_index]]
        return "000"

    def get_jump(self) -> str:
        if self.semicolon_index != -1:
            return JUMP_TABLE[self.assembly_str[self.semicolon_index + 1 :]]
        return "000"

    def get_comp(self) -> str:
        if self.semicolon_index != -1:
            return COMP_TABLE[
                self.assembly_str[self.equal_index + 1 : self.semicolon_index]
            ]
        return COMP_TABLE[self.assembly_str[self.equal_index + 1 :]]


@dataclass
class LInstruction(Instruction):
    def get_bits(self) -> str:
        return ""


class InstructionFactory(Protocol):
    @classmethod
    def __call__(cls, instruction_str: str) -> Instruction:
        pass


class ACLFactory(InstructionFactory):
    @classmethod
    def get_instruction(cls, instruction_str: str) -> Instruction:
        if instruction_str.startswith("@"):
            return AInstruction(instruction_str)
        if "(" in instruction_str:
            return LInstruction(instruction_str)
        return CInstruction(instruction_str)

    @classmethod
    def __call__(cls, instruction_str: str) -> Instruction:
        return cls.get_instruction(instruction_str)
