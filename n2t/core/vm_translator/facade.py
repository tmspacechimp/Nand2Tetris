from dataclasses import dataclass, field
from typing import Iterable

from n2t.core.util.parser import DeleteCommentAndStrip, InstructionParser
from n2t.core.util.trash_filter import CompositeTrashFilter, TrashFilter
from n2t.core.vm_translator.constants import SYS_INIT_CALL
from n2t.core.vm_translator.instruction_factory import StackInstructionFactory
from n2t.core.vm_translator.stack_instruction import BootInstruction, TranslationData


@dataclass
class VMTranslator:
    trash_filter: TrashFilter = field(default_factory=CompositeTrashFilter)
    parser: InstructionParser = field(default_factory=DeleteCommentAndStrip)
    translation_data: TranslationData = field(default_factory=TranslationData)

    def translate_boot(self) -> Iterable[str]:
        stack_instruction = map(
            lambda string: BootInstruction.create(SYS_INIT_CALL, self.translation_data),
            [SYS_INIT_CALL],
        )
        translated = map(lambda instruction: instruction.translate(), stack_instruction)
        return translated

    def translate(self, vm: Iterable[str], file_name: str) -> Iterable[str]:
        self.translation_data.file_name = file_name
        parsed_vm = map(self.parser, filter(self.trash_filter.passes, vm))
        instructions = map(
            lambda stack_str: StackInstructionFactory.build(
                stack_str, self.translation_data
            ),
            parsed_vm,
        )
        translated = map(lambda instruction: instruction.translate(), instructions)

        return translated

    @classmethod
    def create(cls) -> "VMTranslator":
        return cls()
