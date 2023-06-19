from __future__ import annotations

from dataclasses import dataclass, field
from itertools import chain
from pathlib import Path
from typing import Iterable, Iterator, Protocol

from n2t.core.vm_translator.facade import VMTranslator
from n2t.infra.io import File, FileFormat


@dataclass
class VmProgram:
    path: Path
    translator: IVMTranslator = field(default_factory=VMTranslator.create)

    @classmethod
    def load_from(cls, file_or_directory_name: str) -> VmProgram:
        return cls(Path(file_or_directory_name))

    def translate(self) -> None:
        if self.path.is_dir():
            self._translate_directory()
        else:
            self._translate_file()

    def _translate_directory(self) -> None:
        asm_file = File(self.path.joinpath(self.path.name + ".asm"))
        content = self.translator.translate_boot()
        for path in self.path.iterdir():
            if str(path).endswith(".vm"):
                content = chain(
                    content,
                    self.translator.translate(
                        self._iterate_file(path), path.name.removesuffix(".vm")
                    ),
                )
        asm_file.save(content)

    def _translate_file(self) -> None:
        asm_file = File(FileFormat.asm.convert(self.path))
        content = self.translator.translate(self, self.path.name.removesuffix(".vm"))
        asm_file.save(content)

    @classmethod
    def _iterate_file(cls, path: Path) -> Iterator[str]:
        yield from File(path).load()

    def __iter__(self) -> Iterator[str]:
        yield from File(self.path).load()


class IVMTranslator(Protocol):  # pragma: no cover
    def translate_boot(self) -> Iterable[str]:
        pass

    def translate(self, assembly: Iterable[str], file_name: str) -> Iterable[str]:
        pass
