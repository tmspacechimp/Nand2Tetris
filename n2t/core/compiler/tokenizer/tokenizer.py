from itertools import chain
from typing import Iterable, Iterator, Protocol

from n2t.core.compiler.tokenizer.token import ITokenFactory, Token, XMLTokenFactory


class IStepTokenizer(Protocol):
    def get_current(self) -> Token:
        pass

    def get_next(self) -> Token:
        pass

    def has_next(self) -> bool:
        pass


class StepTokenizer(IStepTokenizer):
    jack_iterator: Iterator[str]
    current: Token | None = None
    next: Token | None = None
    token_factory: ITokenFactory = XMLTokenFactory

    def __init__(self, jack_strs: Iterable[str]) -> None:
        self.jack_iterator = iter(chain(jack_strs))
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

    def _update_values(self) -> None:
        self.current = self.next
        try:
            self.next = self._tokenize_word(next(self.jack_iterator))
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

    def has_next(self) -> bool:
        return self.next is not None

    def _tokenize_word(self, jack_str: str) -> Token:
        return self.token_factory.build(jack_str)
