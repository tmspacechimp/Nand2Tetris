import re
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List, Protocol, Type

from n2t.core.compiler.tokenizer.constants import (
    IDENTIFIER_REGEX,
    IDENTIFIER_TYPE_NAME,
    INT_CONSTANT_REGEX,
    INT_CONSTANT_TYPE_NAME,
    KEYWORD_TYPE_NAME,
    KEYWORDS_REGEX,
    STR_CONSTANT_REGEX,
    STR_CONSTANT_TYPE_NAME,
    SYMBOL_TYPE_NAME,
    SYMBOLS_REGEX,
    XML_TOKEN_FORMAT,
)


@dataclass
class Token(ABC):
    jack_str: str

    @abstractmethod
    def get_token(self) -> str:
        pass

    @classmethod
    def create(cls, jack_str: str) -> "Token":
        return cls(jack_str)


class XMLToken(Token):
    format_str: str = XML_TOKEN_FORMAT
    type_name: str

    def get_token(self) -> str:
        return self.format_str.format(type=self.type_name, word=self.jack_str)


class KeywordXMLToken(XMLToken):
    type_name: str = KEYWORD_TYPE_NAME


class SymbolXMLToken(XMLToken):
    type_name: str = SYMBOL_TYPE_NAME


class IdentifierXMLToken(XMLToken):
    type_name: str = IDENTIFIER_TYPE_NAME


class IntegerConstantXMLToken(XMLToken):
    type_name: str = INT_CONSTANT_TYPE_NAME


class StringConstantXMLToken(XMLToken):
    type_name: str = STR_CONSTANT_TYPE_NAME


class ITokenFactory(Protocol):
    @classmethod
    def build(cls, jack_str: str) -> Token:
        pass


class XMLTokenFactory(ITokenFactory):
    regexes: List[str] = [
        KEYWORDS_REGEX,
        SYMBOLS_REGEX,
        IDENTIFIER_REGEX,
        INT_CONSTANT_REGEX,
        STR_CONSTANT_REGEX,
    ]
    object_map: Dict[str, Type[Token]] = {
        KEYWORDS_REGEX: KeywordXMLToken,
        SYMBOLS_REGEX: SymbolXMLToken,
        IDENTIFIER_REGEX: IdentifierXMLToken,
        INT_CONSTANT_REGEX: IntegerConstantXMLToken,
        STR_CONSTANT_REGEX: StringConstantXMLToken,
    }

    @classmethod
    def build(cls, jack_str: str) -> Token:
        for regex in cls.regexes:
            if re.fullmatch(regex, jack_str):
                return cls.object_map.get(regex).create(jack_str)  # type: ignore
        raise Exception
