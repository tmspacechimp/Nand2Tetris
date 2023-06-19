from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable

from n2t.core.assembler.constants import PREDEDINED_SYMBOLS_TABLE
from n2t.core.assembler.instruction import ACLFactory, InstructionFactory, LInstruction
from n2t.core.assembler.util import (
    AfterReservedCounter,
    InstructionCounter,
    LabelAddressGenerator,
    SymbolAddressGenerator,
)
from n2t.core.util.parser import DeleteCommentAndStrip, InstructionParser
from n2t.core.util.trash_filter import CompositeTrashFilter, TrashFilter


@dataclass
class Assembler:
    trash_filter: TrashFilter = field(default_factory=CompositeTrashFilter)
    instruction_factory: InstructionFactory = field(default_factory=ACLFactory)
    parser: InstructionParser = field(default_factory=DeleteCommentAndStrip)
    label_addresses_generator: LabelAddressGenerator = field(
        default_factory=InstructionCounter
    )
    symbol_addresses_generator: SymbolAddressGenerator = field(
        default_factory=AfterReservedCounter
    )

    @classmethod
    def create(cls) -> Assembler:
        return cls()

    def assemble(self, assembly: Iterable[str]) -> Iterable[str]:
        parsed_assembly = map(self.parser, filter(self.trash_filter.passes, assembly))

        instructions = map(self.instruction_factory, parsed_assembly)

        instructions_cache = list(instructions)
        label_addresses = self.label_addresses_generator(instructions_cache)
        symbol_addresses = self.symbol_addresses_generator(
            instructions_cache, label_addresses
        )
        addresses = dict(PREDEDINED_SYMBOLS_TABLE | label_addresses | symbol_addresses)
        ac_instructions = filter(
            lambda instruction: not isinstance(instruction, LInstruction),
            instructions_cache,
        )
        ac_instructions_mapped = map(
            lambda instruction: instruction.set_addresses(addresses), ac_instructions
        )
        binary = map(lambda instruction: instruction.get_bits(), ac_instructions_mapped)
        return binary
