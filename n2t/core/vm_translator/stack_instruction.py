from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import ClassVar

from n2t.core.vm_translator.constants import (
    BINARY_OPERATION_FORMAT,
    BINARY_SYMBOLS_TABLE,
    BOOT_FORMAT,
    BRANCH_OPERATION_FORMAT,
    FUNCTION_CALL_FORMAT,
    FUNCTION_DECLARATION_NAME_PREFIX,
    FUNCTION_DECLARATION_SEGMENT_FORMAT,
    GOTO_FORMAT,
    IF_GOTO_FORMAT,
    LABEL_FORMAT,
    NEGATION_FORMAT,
    NEGATION_SYMBOLS_TABLE,
    RETURN_FORMAT,
    RETURN_LABEL_FORMAT,
)


@dataclass
class TranslationData:
    file_name: str = field(default="")
    branching_counter: int = field(default=0)
    return_counter: int = field(default=0)


@dataclass
class StackInstruction(ABC):
    stack_str: str
    data: TranslationData

    @abstractmethod
    def translate(self) -> str:
        pass

    @classmethod
    def create(cls, stack_str: str, data: TranslationData) -> "StackInstruction":
        return cls(stack_str, data)


class BinaryOperation(StackInstruction):
    format_str: ClassVar[str] = BINARY_OPERATION_FORMAT

    def translate(self) -> str:
        operator = BINARY_SYMBOLS_TABLE.get(self.stack_str.split()[0])
        return self.format_str.format(operator=operator)


class Negation(StackInstruction):
    format_str: ClassVar[str] = NEGATION_FORMAT

    def translate(self) -> str:
        operator = NEGATION_SYMBOLS_TABLE.get(self.stack_str.split()[0])
        return self.format_str.format(operator=operator)


class BranchOperation(StackInstruction):
    format_str: ClassVar[str] = BRANCH_OPERATION_FORMAT

    def translate(self) -> str:
        self.data.branching_counter += 1
        operator = self.stack_str.split()[0].upper()
        return self.format_str.format(
            operator=operator, branching_counter=self.data.branching_counter
        )


class PushOperation(StackInstruction, ABC):
    pass


class PopOperation(StackInstruction, ABC):
    pass


class GotoInstruction(StackInstruction):
    goto_format: ClassVar[str] = GOTO_FORMAT
    if_goto_format: ClassVar[str] = IF_GOTO_FORMAT

    def translate(self) -> str:
        split = self.stack_str.split()
        keyword = split[0]
        label = split[1]
        if keyword == "goto":
            return self.goto_format.format(label=label)
        return self.if_goto_format.format(label=label)


class FunctionDeclaration(StackInstruction):
    prefix_format: ClassVar[str] = FUNCTION_DECLARATION_NAME_PREFIX
    arg_segment_format: ClassVar[str] = FUNCTION_DECLARATION_SEGMENT_FORMAT

    def translate(self) -> str:
        split = self.stack_str.split()
        function_name = split[1]
        num_arguments = int(split[2])
        prefix = self.prefix_format.format(function_name=function_name)
        return prefix + self.arg_segment_format * num_arguments


class FunctionCall(StackInstruction):
    format_str: ClassVar[str] = FUNCTION_CALL_FORMAT
    return_label: ClassVar[str] = RETURN_LABEL_FORMAT

    def translate(self) -> str:
        self.data.return_counter += 1
        split = self.stack_str.split()
        function_name = split[1]
        num_arguments = split[2]
        return_label = self.return_label.format(
            function_name=function_name, return_counter=self.data.return_counter
        )
        return self.format_str.format(
            function_name=function_name,
            num_arguments=num_arguments,
            return_label=return_label,
        )


class ReturnInstruction(StackInstruction):
    format_str: ClassVar[str] = RETURN_FORMAT

    def translate(self) -> str:
        return self.format_str


class BootInstruction(StackInstruction):
    format_str: ClassVar[str] = BOOT_FORMAT

    def translate(self) -> str:
        function_call = FunctionCall.create(self.stack_str, self.data).translate()
        return self.format_str.format(function_call=function_call)


class LabelInstruction(StackInstruction):
    format_str: ClassVar[str] = LABEL_FORMAT

    def translate(self) -> str:
        label_name = self.stack_str.split()[1]
        return self.format_str.format(label_name=label_name)


class TrashInstruction(StackInstruction):
    def translate(self) -> str:
        return ""
