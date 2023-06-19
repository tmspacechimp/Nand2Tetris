from typing import Dict

ADDRESS_TYPE_TABLE: Dict[str, str] = {
    "local": "LCL",
    "argument": "ARG",
    "this": "THIS",
    "that": "THAT",
    "static": "static",
}

BINARY_SYMBOLS_TABLE: Dict[str, str] = {
    "add": "+",
    "sub": "-",
    "and": "&",
    "or": "|",
}

NEGATION_SYMBOLS_TABLE: Dict[str, str] = {"not": "!", "neg": "-"}

BINARY_OPERATION_FORMAT: str = "\n".join(
    [
        "@SP",
        "A=M-1",
        "D=M",
        "A=A-1",
        "M=M{operator}D",
        "@SP",
        "M=M-1",
        "",
    ]
)

NEGATION_FORMAT: str = "\n".join(
    [
        "@SP",
        "A=M-1",
        "M={operator}M",
        "",
    ]
)

BRANCH_OPERATION_FORMAT: str = "\n".join(
    [
        "@SP",
        "A=M-1",
        "D=M",
        "A=A-1",
        "D=M-D",
        "@TRUE{branching_counter}",
        "D;J{operator}",
        "@SP",
        "A=M-1",
        "A=A-1",
        "M=0",
        "@END{branching_counter}",
        "0;JMP",
        "(TRUE{branching_counter})",
        "@SP",
        "A=M-1",
        "A=A-1",
        "M=-1",
        "(END{branching_counter})",
        "@SP",
        "M=M-1",
        "",
    ]
)

POINTER_PUSH_FORMAT: str = "\n".join(
    [
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "",
    ]
)

TEMP_PUSH_FORMAT: str = "\n".join(
    [
        "@5",
        "D=A",
        "@{num}",
        "A=D+A",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "",
    ]
)

CONSTANT_PUSH_FORMAT: str = "\n".join(
    [
        "@{num}",
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "",
    ]
)

STATIC_PUSH_FORMAT: str = "\n".join(
    [
        "@{file_name}.{num}",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "",
    ]
)

NON_STATIC_PUSH_FORMAT: str = "\n".join(
    [
        "@{address_type}",
        "D=M",
        "@{num}",
        "A=D+A",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "",
    ]
)

NON_STATIC_POP_FORMAT: str = "\n".join(
    [
        "@{address_type}",
        "D=M",
        "@{num}",
        "D=D+A",
        "@13",
        "M=D",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@13",
        "A=M",
        "M=D",
        "",
    ]
)

STATIC_POP_FORMAT: str = "\n".join(
    [
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@{file_name}.{num}",
        "M=D",
        "",
    ]
)

TEMP_POP_FORMAT: str = "\n".join(
    [
        "@5",
        "D=A",
        "@{num}",
        "D=D+A",
        "@13",
        "M=D",
        "@SP",
        "M=M-1",
        "A=M",
        "D=M",
        "@13",
        "A=M",
        "M=D",
        "",
    ]
)

THAT_POINTER_POP_FORMAT: str = "\n".join(
    ["@SP", "M=M-1", "A=M", "D=M", "@THAT", "M=D", ""]
)

THIS_POINTER_POP_FORMAT: str = "\n".join(
    ["@SP", "M=M-1", "A=M", "D=M", "@THIS", "M=D", ""]
)

RETURN_FORMAT: str = "\n".join(
    [
        "@LCL",
        "D=M",
        "@5",
        "D=D-A",
        "A=D",
        "D=M",
        "@13",
        "M=D",
        "@SP",
        "A=M-1",
        "D=M",
        "@ARG",
        "A=M",
        "M=D",
        "@SP",
        "M=M-1",
        "@ARG",
        "D=M+1",
        "@SP",
        "M=D",
        "@LCL",
        "D=M",
        "@1",
        "D=D-A",
        "A=D",
        "D=M",
        "@THAT",
        "M=D",
        "@LCL",
        "D=M",
        "@2",
        "D=D-A",
        "A=D",
        "D=M",
        "@THIS",
        "M=D",
        "@LCL",
        "D=M",
        "@3",
        "D=D-A",
        "A=D",
        "D=M",
        "@ARG",
        "M=D",
        "@LCL",
        "D=M",
        "@4",
        "D=D-A",
        "A=D",
        "D=M",
        "@LCL",
        "M=D",
        "@13",
        "A=M",
        "0;JMP",
        "",
    ]
)

FUNCTION_CALL_FORMAT: str = "\n".join(
    [
        "@{return_label}",
        "D=A",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@LCL",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@ARG",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@THIS",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@THAT",
        "D=M",
        "@SP",
        "A=M",
        "M=D",
        "@SP",
        "M=M+1",
        "@SP",
        "D=M",
        "@5",
        "D=D-A",
        "@{num_arguments}",
        "D=D-A",
        "@ARG",
        "M=D",
        "@SP",
        "D=M",
        "@LCL",
        "M=D",
        "@{function_name}",
        "0;JMP",
        "({return_label})",
        "",
    ]
)

RETURN_LABEL_FORMAT: str = "RETURN.{function_name}.{return_counter}"

GOTO_FORMAT: str = "\n".join(["@{label}", "0;JMP", ""])

IF_GOTO_FORMAT: str = "\n".join(["@SP", "M=M-1", "A=M", "D=M", "@{label}", "D;JNE", ""])

BOOT_FORMAT: str = "\n".join(["@256", "D=A", "@SP", "M=D", "{function_call}"])

SYS_INIT_CALL: str = "call Sys.init 0"

FUNCTION_DECLARATION_SEGMENT_FORMAT: str = "\n".join(
    ["@SP", "A=M", "M=0", "@SP", "M=M+1", ""]
)

FUNCTION_DECLARATION_NAME_PREFIX: str = "\n".join(["({function_name})", ""])

LABEL_FORMAT: str = "\n".join(["({label_name})", ""])
