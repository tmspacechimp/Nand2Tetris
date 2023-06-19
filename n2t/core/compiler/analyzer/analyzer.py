from typing import Iterable, Protocol

from n2t.core.compiler.tokenizer.tokenizer import IStepTokenizer


class FragmentAnalyzer(Protocol):
    @classmethod
    def analyze(cls, tokenizer: IStepTokenizer, depth: int) -> Iterable[str]:
        pass
