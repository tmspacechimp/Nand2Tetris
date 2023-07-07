from typing import Protocol

from n2t.core.compiler.constants import (
    FUNCTION_CALL_FORMAT,
    FUNCTION_DEC_FORMAT,
    GOTO_FORMAT,
    IF_FORMAT,
    LABEL_FORMAT,
    OPERATION_FORMAT,
    POP_FORMAT,
    PUSH_FORMAT,
    RETURN_FORMAT,
)


class IVMFormatter(Protocol):
    @classmethod
    def get_pop(cls, pop_type: str, index: int) -> str:
        pass

    @classmethod
    def get_push(cls, push_type: str, index: int) -> str:
        pass

    @classmethod
    def get_label(cls, label_name: str) -> str:
        pass

    @classmethod
    def get_if(cls, label_name: str) -> str:
        pass

    @classmethod
    def get_goto(cls, label_name: str) -> str:
        pass

    @classmethod
    def get_function_dec(cls, name: str, num_args: int) -> str:
        pass

    @classmethod
    def get_function_call(cls, name: str, num_args: int) -> str:
        pass

    @classmethod
    def get_return_statement(cls) -> str:
        pass

    @classmethod
    def get_operation(cls, operation: str) -> str:
        pass


class VMFormatter(IVMFormatter):
    @classmethod
    def get_pop(cls, pop_type: str, index: int) -> str:
        return POP_FORMAT.format(type=pop_type, index=index)

    @classmethod
    def get_push(cls, push_type: str, index: int) -> str:
        return PUSH_FORMAT.format(type=push_type, index=index)

    @classmethod
    def get_label(cls, name: str) -> str:
        return LABEL_FORMAT.format(name=name)

    @classmethod
    def get_if(cls, label_name: str) -> str:
        return IF_FORMAT.format(label=label_name)

    @classmethod
    def get_goto(cls, label_name: str) -> str:
        return GOTO_FORMAT.format(label=label_name)

    @classmethod
    def get_function_dec(cls, name: str, num_args: int) -> str:
        return FUNCTION_DEC_FORMAT.format(name=name, num_args=num_args)

    @classmethod
    def get_function_call(cls, name: str, num_args: int) -> str:
        return FUNCTION_CALL_FORMAT.format(name=name, num_args=num_args)

    @classmethod
    def get_return_statement(cls) -> str:
        return RETURN_FORMAT

    @classmethod
    def get_operation(cls, operation: str) -> str:
        return OPERATION_FORMAT.format(operation=operation)
