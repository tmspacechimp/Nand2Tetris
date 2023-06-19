from typing import Dict, FrozenSet, Set, Type

from n2t.core.vm_translator.pop_polymorphics import PopOperationFactoryAdapter
from n2t.core.vm_translator.push_polymorphics import PushOperationFactoryAdapter
from n2t.core.vm_translator.stack_instruction import (
    BinaryOperation,
    BranchOperation,
    FunctionCall,
    FunctionDeclaration,
    GotoInstruction,
    LabelInstruction,
    Negation,
    ReturnInstruction,
    StackInstruction,
    TranslationData,
    TrashInstruction,
)


class StackInstructionFactory:
    binary_keywords: FrozenSet[str] = frozenset({"add", "sub", "and", "or"})
    negation_keywords: FrozenSet[str] = frozenset({"not", "neg"})
    branching_keywords: FrozenSet[str] = frozenset({"eq", "lt", "gt"})
    push_keywords: FrozenSet[str] = frozenset({"push"})
    pop_keywords: FrozenSet[str] = frozenset({"pop"})
    label_keywords: FrozenSet[str] = frozenset({"label"})
    function_declaration_keywords: FrozenSet[str] = frozenset({"function"})
    function_call_keywords: FrozenSet[str] = frozenset({"call"})
    return_keywords: FrozenSet[str] = frozenset({"return"})
    goto_keywords: FrozenSet[str] = frozenset({"goto", "if-goto"})
    keyword_types: Set[FrozenSet[str]] = {
        binary_keywords,
        negation_keywords,
        branching_keywords,
        push_keywords,
        pop_keywords,
        label_keywords,
        function_declaration_keywords,
        function_call_keywords,
        return_keywords,
        goto_keywords,
    }
    operation_objects: Dict[FrozenSet[str], Type[StackInstruction]] = {
        binary_keywords: BinaryOperation,
        negation_keywords: Negation,
        branching_keywords: BranchOperation,
        push_keywords: PushOperationFactoryAdapter,
        pop_keywords: PopOperationFactoryAdapter,
        label_keywords: LabelInstruction,
        function_declaration_keywords: FunctionDeclaration,
        function_call_keywords: FunctionCall,
        return_keywords: ReturnInstruction,
        goto_keywords: GotoInstruction,
    }

    @classmethod
    def build(cls, stack_str: str, data: TranslationData) -> StackInstruction:
        operator = stack_str.split()[0]
        for keywords in cls.keyword_types:
            if operator in keywords:
                return cls.operation_objects[keywords].create(stack_str, data)
        return TrashInstruction.create(stack_str, data)
