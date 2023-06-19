from typing import Dict, Iterable, Protocol

from n2t.core.assembler.constants import PREDEDINED_SYMBOLS_TABLE
from n2t.core.assembler.instruction import AInstruction, Instruction, LInstruction


class LabelAddressGenerator(Protocol):
    @classmethod
    def __call__(cls, instructions: Iterable[Instruction]) -> Dict[str, int]:
        pass


class SymbolAddressGenerator(Protocol):
    @classmethod
    def __call__(
        cls, instructions: Iterable[Instruction], labels: Dict[str, int]
    ) -> Dict[str, int]:
        pass


class InstructionCounter(LabelAddressGenerator):
    @classmethod
    def generate(cls, instructions: Iterable[Instruction]) -> Dict[str, int]:
        table = {}
        address = 0
        for instruction in instructions:
            if isinstance(instruction, LInstruction):
                table[instruction.assembly_str[1:-1]] = address
                continue
            address += 1
        return table

    @classmethod
    def __call__(cls, instructions: Iterable[Instruction]) -> Dict[str, int]:
        return cls.generate(instructions)


class AfterReservedCounter(SymbolAddressGenerator):
    @classmethod
    def generate(
        cls, instructions: Iterable[Instruction], labels: Dict[str, int]
    ) -> Dict[str, int]:
        table = dict(PREDEDINED_SYMBOLS_TABLE | labels)
        index = 15
        for instruction in instructions:
            if (
                isinstance(instruction, AInstruction)
                and not instruction.assembly_str[1:].isdecimal()
            ):
                symbol = instruction.assembly_str[1:]
                if symbol not in table:
                    index += 1
                    table[symbol] = index
        return table

    @classmethod
    def __call__(
        cls, instructions: Iterable[Instruction], labels: Dict[str, int]
    ) -> Dict[str, int]:
        return cls.generate(instructions, labels)
