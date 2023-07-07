from typing import Dict, Iterable

POP_FORMAT: str = "pop {type} {index}\n"
PUSH_FORMAT: str = "push {type} {index}\n"
LABEL_FORMAT: str = "label {name}\n"
GOTO_FORMAT: str = "goto {label}\n"
IF_FORMAT: str = "if-goto {label}\n"
FUNCTION_DEC_FORMAT: str = "function {name} {num_args}\n"
FUNCTION_CALL_FORMAT: str = "call {name} {num_args}\n"
RETURN_FORMAT: str = "return\n"
OPERATION_FORMAT: str = "{operation}\n"
STATEMENT_KEYWORDS: Iterable[str] = ("do", "let", "if", "while", "return")
OPERATOR_KEYWORDS: Iterable[str] = (
    "+",
    "-",
    "=",
    "*",
    "/",
    "|",
    "&amp;",
    "&lt;",
    "&gt;",
)
OPERATOR_VM_NAMES: Dict[str, str] = {
    "+": "add",
    "-": "sub",
    "=": "eq",
    "*": "Math.multiply",
    "/": "Math.divide",
    "|": "or",
    "&amp;": "and",
    "&lt;": "lt",
    "&gt;": "gt",
}
