from abc import ABC
from dataclasses import dataclass
from typing import ClassVar, Dict, Type

from n2t.core.vm_translator.constants import (
    CONSTANT_PUSH_FORMAT,
    NON_STATIC_PUSH_FORMAT,
    POINTER_PUSH_FORMAT,
    STATIC_PUSH_FORMAT,
    TEMP_PUSH_FORMAT,
    ADDRESS_TYPE_TABLE,
)
from n2t.core.vm_translator.stack_instruction import (
    PushOperation,
    StackInstruction,
    TranslationData,
)


@dataclass
class PointerPushOperation(PushOperation):
    this_prefix: ClassVar[str] = "@THIS\n"
    that_prefix: ClassVar[str] = "@THAT\n"
    format_str: ClassVar[str] = POINTER_PUSH_FORMAT

    def translate(self) -> str:
        if self.stack_str.split()[2] == "0":
            return self.this_prefix + self.format_str
        return self.this_prefix + self.format_str


@dataclass
class TempPushOperation(PushOperation):
    format_str: ClassVar[str] = TEMP_PUSH_FORMAT

    def translate(self) -> str:
        num = self.stack_str.split()[2]
        return self.format_str.format(num=num)


@dataclass
class ConstantPushOperation(PushOperation):
    format_str: ClassVar[str] = CONSTANT_PUSH_FORMAT

    def translate(self) -> str:
        num = self.stack_str.split()[2]
        return self.format_str.format(num=num)


class StaticPushOperation(PushOperation):
    format_str: ClassVar[str] = STATIC_PUSH_FORMAT

    def translate(self) -> str:
        num = self.stack_str.split()[2]
        return self.format_str.format(file_name=self.data.file_name, num=num)


class NonStaticAddressPushOperation(PushOperation):
    format_str: ClassVar[str] = NON_STATIC_PUSH_FORMAT

    def translate(self) -> str:
        split = self.stack_str.split()
        address_type = ADDRESS_TYPE_TABLE.get(split[1])
        num = split[2]
        return self.format_str.format(address_type=address_type, num=num)


class PushOperationFactory:
    push_objects: ClassVar[Dict[str, Type[PushOperation]]] = {
        "pointer": PointerPushOperation,
        "temp": TempPushOperation,
        "constant": ConstantPushOperation,
        "static": StaticPushOperation,
    }

    @classmethod
    def build(cls, stack_str: str, data: TranslationData) -> StackInstruction:
        keyword = stack_str.split()[1]
        if keyword in cls.push_objects:
            return cls.push_objects[keyword].create(stack_str, data)
        return NonStaticAddressPushOperation.create(stack_str, data)


class PushOperationFactoryAdapter(PushOperation, ABC):
    @classmethod
    def create(cls, stack_str: str, data: TranslationData) -> StackInstruction:
        return PushOperationFactory.build(stack_str, data)
