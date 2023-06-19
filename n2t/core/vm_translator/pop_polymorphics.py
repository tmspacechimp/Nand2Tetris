from abc import ABC
from typing import ClassVar, Dict, Type

from n2t.core.vm_translator.constants import (
    NON_STATIC_POP_FORMAT,
    STATIC_POP_FORMAT,
    TEMP_POP_FORMAT,
    THAT_POINTER_POP_FORMAT,
    THIS_POINTER_POP_FORMAT,
    ADDRESS_TYPE_TABLE,
)
from n2t.core.vm_translator.stack_instruction import (
    PopOperation,
    StackInstruction,
    TranslationData,
)


class PointerPopOperation(PopOperation):
    this_format_str: ClassVar[str] = THIS_POINTER_POP_FORMAT
    that_format_str: ClassVar[str] = THAT_POINTER_POP_FORMAT

    def translate(self) -> str:
        if self.stack_str.split()[2] == "0":
            return self.this_format_str
        return self.that_format_str


class TempPopOperation(PopOperation):
    format_str: ClassVar[str] = TEMP_POP_FORMAT

    def translate(self) -> str:
        num = self.stack_str.split()[2]
        return self.format_str.format(num=num)


class StaticPopOperation(PopOperation):
    format_str: ClassVar[str] = STATIC_POP_FORMAT

    def translate(self) -> str:
        num = self.stack_str.split()[2]
        return self.format_str.format(file_name=self.data.file_name, num=num)


class NonStaticAddressPopOperation(PopOperation):
    format_str: ClassVar[str] = NON_STATIC_POP_FORMAT

    def translate(self) -> str:
        split = self.stack_str.split()
        address_type = ADDRESS_TYPE_TABLE.get(split[1])
        num = split[2]
        return self.format_str.format(address_type=address_type, num=num)


class PopOperationFactory:
    pop_objects: ClassVar[Dict[str, Type["PopOperation"]]] = {
        "pointer": PointerPopOperation,
        "temp": TempPopOperation,
        "static": StaticPopOperation,
    }

    @classmethod
    def build(cls, stack_str: str, data: TranslationData) -> StackInstruction:
        keyword = stack_str.split()[1]
        if keyword in cls.pop_objects:
            return cls.pop_objects[keyword].create(stack_str, data)
        return NonStaticAddressPopOperation.create(stack_str, data)


class PopOperationFactoryAdapter(PopOperation, ABC):
    @classmethod
    def create(cls, stack_str: str, data: TranslationData) -> StackInstruction:
        return PopOperationFactory.build(stack_str, data)
