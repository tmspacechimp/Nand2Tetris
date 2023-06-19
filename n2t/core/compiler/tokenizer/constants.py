import re

KEYWORDS = "|".join(
    {
        "class",
        "constructor",
        "function",
        "method",
        "field",
        "static",
        "var",
        "int",
        "char",
        "boolean",
        "void",
        "true",
        "false",
        "null",
        "this",
        "let",
        "do",
        "if",
        "else",
        "while",
        "return",
    }
)

KEYWORDS_REGEX = r"^(" + KEYWORDS + r")$"

SYMBOLS = "|".join(
    map(
        re.escape,
        {
            "{",
            "}",
            "(",
            ")",
            "[",
            "]",
            ".",
            ",",
            ";",
            "+",
            "-",
            "*",
            "/",
            "&",
            "|",
            "<",
            ">",
            "=",
            "~",
        },
    )
)

SYMBOLS_REGEX = r"^(" + SYMBOLS + r")$"

IDENTIFIER_REGEX = r"(_|[a-z]|[A-Z])\w*"

INT_CONSTANT_REGEX = r"\d+"

STR_CONSTANT_REGEX = r"\"(.*?)\""

XML_TOKEN_FORMAT = "<{type}> {word} </{type}>\n"

KEYWORD_TYPE_NAME = "keyword"

SYMBOL_TYPE_NAME = "symbol"

IDENTIFIER_TYPE_NAME = "identifier"

INT_CONSTANT_TYPE_NAME = "integerConstant"

STR_CONSTANT_TYPE_NAME = "stringConstant"
