from dataclasses import dataclass, field
from functools import reduce
from itertools import chain
from typing import Iterable, Type

from n2t.core.compiler.compiler import ClassCompiler, IClassCompiler
from n2t.core.util.parser import (
    DeleteCommentAndStrip,
    IJackSplitter,
    InstructionParser,
    JackSplitter,
)
from n2t.core.util.trash_filter import CompositeTrashFilter, TrashFilter


@dataclass
class JackCompiler:
    class_compiler: Type[IClassCompiler] = ClassCompiler
    trash_filter: TrashFilter = field(default_factory=CompositeTrashFilter)
    parser: InstructionParser = field(default_factory=DeleteCommentAndStrip)
    splitter: IJackSplitter = field(default_factory=JackSplitter)

    def compile(self, jack_strs: Iterable[str]) -> Iterable[str]:
        parsed = map(self.parser, filter(self.trash_filter.passes, jack_strs))
        split = map(self.splitter, parsed)
        flat = reduce(chain, split)
        return self.class_compiler.create(flat).compile_class()

    @classmethod
    def create(cls) -> "JackCompiler":
        return cls()
