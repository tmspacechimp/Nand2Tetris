from dataclasses import dataclass, field
from typing import Callable, Dict, Iterable, List, Protocol

from n2t.core.compiler.constants import (
    OPERATOR_KEYWORDS,
    OPERATOR_VM_NAMES,
    STATEMENT_KEYWORDS,
)
from n2t.core.compiler.namespace import INameSpace, NameSpace
from n2t.core.compiler.tokenizer.token import (
    IdentifierXMLToken,
    IntegerConstantXMLToken,
    KeywordXMLToken,
)
from n2t.core.compiler.tokenizer.tokenizer import (
    IStepTokenizer,
    StepTokenizerForJackCompiler,
)
from n2t.core.compiler.vm_formatter import IVMFormatter, VMFormatter


@dataclass
class SubroutineData:
    name: str = ""
    of_type: str = ""


class IClassCompiler(Protocol):
    def compile_class(self) -> Iterable[str]:
        pass

    @classmethod
    def create(cls, jack_strs: Iterable[str]) -> "IClassCompiler":
        pass


@dataclass
class ClassCompiler:
    vm: List[str] = field(init=False)
    jack_strs: Iterable[str] = field(init=True)
    tokenizer: IStepTokenizer = field(init=False)
    namespace: INameSpace = field(default_factory=NameSpace)
    label_cnt: int = field(init=False, default=0)
    name: str = field(init=False, default_factory=str)
    current_subroutine: SubroutineData = field(
        init=False, default_factory=SubroutineData
    )
    vm_formatter: IVMFormatter = field(default=VMFormatter)
    statement_keywords: Iterable[str] = field(init=False, default=STATEMENT_KEYWORDS)
    statement_compiler_methods: Dict[str, Callable[[], None]] = field(init=False)
    operator_keywords: Iterable[str] = field(default=OPERATOR_KEYWORDS)

    def __post_init__(self) -> None:
        self.tokenizer = StepTokenizerForJackCompiler(jack_strs=self.jack_strs)
        self.statement_compiler_methods = {
            "do": self.compile_do_statement,
            "let": self.compile_let_statement,
            "if": self.compile_if_statement,
            "return": self.compile_return_statement,
            "while": self.compile_while_statement,
        }
        self.operator_vm_names = OPERATOR_VM_NAMES
        self.vm = []

    @classmethod
    def create(cls, jack_strs: Iterable[str]) -> "ClassCompiler":
        return cls(jack_strs)

    def compile_class(self) -> Iterable[str]:
        self.vm = []
        self.label_cnt = 0
        self.name = self.tokenizer.get_next().jack_str
        self.tokenizer.take_steps(2)
        while self.tokenizer.get_current().jack_str in ["static", "field"]:
            self.compile_class_vars()

        while self.tokenizer.get_current().jack_str in [
            "constructor",
            "method",
            "function",
        ]:
            self.compile_subroutine()

        return self.vm

    def compile_class_vars(self) -> None:
        scope = self.tokenizer.get_current().jack_str
        of_type = self.tokenizer.get_next().jack_str
        while True:
            name = self.tokenizer.get_next().jack_str
            self.namespace.define(name, scope, of_type)
            self.tokenizer.take_steps(1)
            if self.tokenizer.get_current().jack_str != ",":
                self.tokenizer.take_steps(1)
                break

    def compile_subroutine(self) -> None:
        self.compile_subroutine_dec()
        self.tokenizer.take_steps(1)
        self.compile_args()
        self.tokenizer.take_steps(1)
        self.compile_subroutine_body()

    def compile_subroutine_dec(self) -> None:
        self.namespace.init_sub()
        of_type = self.tokenizer.get_current().jack_str
        self.current_subroutine.of_type = of_type
        if of_type == "method":
            self.namespace.define("this", "argument", self.name)
        self.tokenizer.take_steps(2)
        self.current_subroutine.name = self.tokenizer.get_current().jack_str
        self.tokenizer.take_steps(1)

    # starts after (
    def compile_args(self) -> None:
        token = self.tokenizer.get_current().jack_str
        while token != ")":
            of_type = token
            name = self.tokenizer.get_next().jack_str
            self.namespace.define(name, "argument", of_type)
            if self.tokenizer.get_next().jack_str == ",":
                self.tokenizer.take_steps(1)
            token = self.tokenizer.get_current().jack_str

    # starts from {
    def compile_subroutine_body(self) -> None:
        self.tokenizer.take_steps(1)
        num_locals = self.compile_local_vars()
        self.subroutine_dec_to_vm(num_locals)
        self.compile_statements()
        self.tokenizer.take_steps(1)

    def compile_local_vars(self) -> int:
        num_locals = 0
        while self.tokenizer.get_current().jack_str == "var":
            of_type = self.tokenizer.get_next().jack_str
            while True:
                num_locals += 1
                name = self.tokenizer.get_next().jack_str
                self.namespace.define(name, "local", of_type)
                if self.tokenizer.get_next().jack_str == ";":
                    self.tokenizer.take_steps(1)
                    break

        return num_locals

    def subroutine_dec_to_vm(self, num_locals: int) -> None:
        self.vm.append(
            self.vm_formatter.get_function_dec(
                f"{self.name}.{self.current_subroutine.name}", num_locals
            )
        )
        if self.current_subroutine.of_type == "constructor":
            self.vm.append(
                self.vm_formatter.get_push("constant", self.namespace.count("this"))
            )
            self.vm.append(self.vm_formatter.get_function_call("Memory.alloc", 1))
            self.vm.append(self.vm_formatter.get_pop("pointer", 0))
        if self.current_subroutine.of_type == "method":
            self.vm.append(self.vm_formatter.get_push("argument", 0))
            self.vm.append(self.vm_formatter.get_pop("pointer", 0))

    def compile_statements(self) -> None:
        # if self.tokenizer.get_current().jack_str == ";":
        #     self.tokenizer.take_steps(1)
        while self.tokenizer.get_current().jack_str in STATEMENT_KEYWORDS:
            self.statement_compiler_methods[self.tokenizer.get_current().jack_str]()

    def compile_do_statement(self) -> None:
        self.tokenizer.take_steps(1)
        self.call_subroutine()
        self.vm.append(self.vm_formatter.get_pop("temp", 0))
        self.tokenizer.take_steps(1)

    def compile_let_statement(self) -> None:
        name = self.tokenizer.get_next().jack_str
        data = self.namespace.get(name)
        if self.tokenizer.get_next().jack_str == "[":
            self.tokenizer.take_steps(1)
            self.vm.append(self.vm_formatter.get_push(data.scope, data.index))

            self.compile_expression()

            self.vm.append(self.vm_formatter.get_operation("add"))
            self.tokenizer.take_steps(2)

            self.compile_expression()
            self.vm.append(self.vm_formatter.get_pop("temp", 0))
            self.vm.append(self.vm_formatter.get_pop("pointer", 1))
            self.vm.append(self.vm_formatter.get_push("temp", 0))
            self.vm.append(self.vm_formatter.get_pop("that", 0))
        else:
            self.tokenizer.take_steps(1)
            self.compile_expression()
            self.vm.append(self.vm_formatter.get_pop(data.scope, data.index))

        self.tokenizer.take_steps(1)

    def compile_if_statement(self) -> None:
        l0 = f"L0{self.label_cnt}"
        l1 = f"L1{self.label_cnt}"
        self.label_cnt += 1
        self.tokenizer.take_steps(2)
        self.compile_expression()

        self.vm.append(self.vm_formatter.get_operation("not"))
        self.tokenizer.take_steps(2)

        self.vm.append(self.vm_formatter.get_if(l0))
        self.compile_statements()
        self.vm.append(self.vm_formatter.get_goto(l1))
        self.tokenizer.take_steps(1)
        self.vm.append(self.vm_formatter.get_label(l0))

        if self.tokenizer.get_current().jack_str == "else":
            self.tokenizer.take_steps(2)
            self.compile_statements()
            self.tokenizer.take_steps(1)

        self.vm.append(self.vm_formatter.get_label(l1))

    def compile_while_statement(self) -> None:
        l0 = f"L0{self.label_cnt}"
        l1 = f"L1{self.label_cnt}"
        self.label_cnt += 1

        self.tokenizer.take_steps(2)
        self.vm.append(self.vm_formatter.get_label(l0))
        self.compile_expression()

        self.vm.append(self.vm_formatter.get_operation("not"))
        self.vm.append(self.vm_formatter.get_if(l1))
        self.tokenizer.take_steps(2)
        self.compile_statements()

        self.vm.append(self.vm_formatter.get_goto(l0))
        self.vm.append(self.vm_formatter.get_label(l1))
        self.tokenizer.take_steps(1)

    def compile_return_statement(self) -> None:
        if self.tokenizer.get_next().jack_str == ";":
            self.vm.append(self.vm_formatter.get_push("constant", 0))
        else:
            self.compile_expression()
        self.vm.append(self.vm_formatter.get_return_statement())
        self.tokenizer.take_steps(1)

    def call_subroutine(self) -> None:
        name = self.tokenizer.get_current().jack_str
        self.tokenizer.take_steps(1)
        self.call_subroutine_named(name)

    def call_subroutine_named(self, name: str) -> None:
        class_name = self.name
        num_args = 1
        if self.tokenizer.get_current().jack_str == ".":
            if self.namespace.is_defined(name):
                data = self.namespace.get(name)
                class_name = data.type
                self.vm.append(self.vm_formatter.get_push(data.scope, data.index))
            else:
                num_args = 0
                class_name = name
            name = self.tokenizer.get_next().jack_str
            self.tokenizer.take_steps(1)
        else:
            self.vm.append(self.vm_formatter.get_push("pointer", 0))

        self.tokenizer.take_steps(1)
        num_args += self.compile_expressions()
        self.vm.append(
            self.vm_formatter.get_function_call(f"{class_name}.{name}", num_args)
        )
        self.tokenizer.take_steps(1)

    def compile_expressions(self) -> int:
        num_args = 0
        while self.tokenizer.get_current().jack_str != ")":
            num_args += 1
            self.compile_expression()
            if self.tokenizer.get_current().jack_str == ",":
                self.tokenizer.take_steps(1)
        return num_args

    def compile_expression(self) -> None:
        self.compile_operand()
        operator = self.tokenizer.get_current().jack_str
        while operator in self.operator_keywords:
            self.tokenizer.take_steps(1)
            self.compile_operand()
            vm_operator = self.operator_vm_names[operator]
            if operator in ["*", "/"]:
                self.vm.append(self.vm_formatter.get_function_call(vm_operator, 2))
            else:
                self.vm.append(self.vm_formatter.get_operation(vm_operator))
            operator = self.tokenizer.get_current().jack_str

    def compile_operand(self) -> None:
        token = self.tokenizer.get_current()
        if token.jack_str == "(":
            self.tokenizer.take_steps(1)
            self.compile_expression()
            self.tokenizer.take_steps(1)
        elif token.jack_str in ["-", "~"]:
            self.tokenizer.take_steps(1)
            self.compile_operand()
            vm_operation = self.operator_vm_names[token.jack_str]
            self.vm.append(self.vm_formatter.get_operation(vm_operation))
        elif isinstance(token, IdentifierXMLToken):
            self.compile_identifier()
        else:
            self.compile_constant()

    def compile_identifier(self) -> None:
        name = self.tokenizer.get_current().jack_str
        if self.tokenizer.get_next().jack_str == "[":
            data = self.namespace.get(name)
            self.vm.append(self.vm_formatter.get_push(data.scope, data.index))
            self.tokenizer.take_steps(1)
            self.compile_expression()

            self.vm.append(self.vm_formatter.get_operation("add"))
            self.vm.append(self.vm_formatter.get_pop("pointer", 1))
            self.vm.append(self.vm_formatter.get_push("that", 0))
            self.tokenizer.take_steps(1)
        elif self.tokenizer.get_current().jack_str in ["(", "."]:
            self.call_subroutine_named(name)
        else:
            data = self.namespace.get(name)
            self.vm.append(self.vm_formatter.get_push(data.scope, data.index))

    def compile_constant(self) -> None:
        token = self.tokenizer.get_current()
        if isinstance(token, IntegerConstantXMLToken):
            self.vm.append(self.vm_formatter.get_push("constant", int(token.jack_str)))
        elif isinstance(token, KeywordXMLToken):
            if token.jack_str == "this":
                self.vm.append(self.vm_formatter.get_push("pointer", 0))
            elif token.jack_str == "true":
                self.vm.append(self.vm_formatter.get_push("constant", 0))
                self.vm.append(self.vm_formatter.get_operation("not"))
            else:
                self.vm.append(self.vm_formatter.get_push("constant", 0))
        else:
            size = len(token.jack_str)
            self.vm.append(self.vm_formatter.get_push("constant", size))
            self.vm.append(self.vm_formatter.get_function_call("String.new", 1))
            for c in token.jack_str:
                self.vm.append(self.vm_formatter.get_push("constant", ord(c)))
                self.vm.append(
                    self.vm_formatter.get_function_call("String.appendChar", 2)
                )
        self.tokenizer.take_steps(1)
