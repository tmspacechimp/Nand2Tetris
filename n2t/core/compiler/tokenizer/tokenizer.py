import re
from typing import Iterable, Iterator, Protocol

from n2t.core.compiler.tokenizer.constants import (
    MULTIWORD_STR_CONSTANT_BEGINNING,
    MULTIWORD_STR_CONSTANT_ENDING,
)
from n2t.core.compiler.tokenizer.token import (
    ITokenFactory,
    StringConstantXMLToken,
    SymbolXMLToken,
    Token,
    XMLTokenFactory,
)


class IStepTokenizer(Protocol):
    def get_current(self) -> Token:
        pass

    def get_next(self) -> Token:
        pass

    def has_next(self) -> bool:
        pass

    def take_steps(self, num: int) -> None:
        pass

    def peek(self) -> Token:
        pass


class StepTokenizer(IStepTokenizer):
    jack_iterator: Iterator[str]
    current: Token | None = None
    next: Token | None = None
    token_factory: ITokenFactory = XMLTokenFactory

    def __init__(self, jack_strs: Iterable[str]) -> None:
        self.jack_iterator = iter(jack_strs)
        self._init_values()

    def get_current(self) -> Token:
        if self.current is None:
            raise StopIteration
        return self.current

    def get_next(self) -> Token:
        if self.next is None:
            raise StopIteration
        res = self.next
        self._update_values()
        return res

    def take_steps(self, num: int) -> None:
        for i in range(num):
            self._update_values()

    def peek(self) -> Token:
        if self.next is None:
            raise StopIteration
        return self.next

    def _update_values(self) -> None:
        self.current = self.next
        try:
            word = next(self.jack_iterator)
            if self._is_str_const_beginning(word):
                word = self._get_multiword_constant(word)
            self.next = self._tokenize_word(word)
        except StopIteration:
            self.next = None

    def _init_values(self) -> None:
        try:
            self.current = self._tokenize_word(next(self.jack_iterator))
        except StopIteration:
            pass
        try:
            self.next = self._tokenize_word(next(self.jack_iterator))
        except StopIteration:
            pass

    @classmethod
    def _is_str_const_beginning(cls, word: str) -> bool:
        return bool(re.fullmatch(MULTIWORD_STR_CONSTANT_BEGINNING, word))

    @classmethod
    def _is_str_const_ending(cls, word: str) -> bool:
        return bool(re.fullmatch(MULTIWORD_STR_CONSTANT_ENDING, word))

    def _get_multiword_constant(self, word: str) -> str:
        while True:
            next_word = next(self.jack_iterator)
            word += next_word
            if self._is_str_const_ending(next_word):
                break
        return word

    def has_next(self) -> bool:
        return self.next is not None

    def _tokenize_word(self, jack_str: str) -> Token:
        return self.token_factory.build(jack_str)


def jack_cleanup(token: Token) -> None:
    if isinstance(token, StringConstantXMLToken):
        token.jack_str = token.jack_str.strip('"')
    elif isinstance(token, SymbolXMLToken):
        token.jack_str = (
            token.jack_str.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
            .replace('"', "&quot;")
        )


class StepTokenizerForJackCompiler(StepTokenizer):
    def __init__(self, jack_strs: Iterable[str]) -> None:
        super().__init__(jack_strs)

    def get_current(self) -> Token:
        token = super().get_current()
        jack_cleanup(token)
        return token
