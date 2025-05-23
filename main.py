from Lexer import Lexer
from Parser import Parser
from Compiler import Compiler
from AST import Program
import json

from llvmlite import ir
import llvmlite.binding as llvm
from ctypes import CFUNCTYPE, c_int, c_float

LEXER_DEBUG: bool = False
PARSER_DEBUG: bool = False
COMPILER_DEBUG: bool = True

if __name__ == '__main__':
    with open("tests/compiler.sl", "r") as f:
        code: str = f.read()

    if LEXER_DEBUG:
        debug_lex: Lexer = Lexer(source=code)
        while debug_lex.current_char is not None:
            print(debug_lex.next_token())

    l: Lexer = Lexer(source=code)
    p: Parser = Parser(lexer=l)

    program: Program = p.parse_program()
    if len(p.errors) > 0:
        for err in p.errors:
            print(err)
        exit(1)

    if PARSER_DEBUG:
        print("==== PARSER DEBUG ====")

        with open("debug/ast.json", "w") as f:
            json.dump(program.json(), f, indent=4)

        print("Wrote AST to debug/ast.json successfully")

    c: Compiler = Compiler()
    c.compile(node=program)

    # Output steps
    module: ir.Module = c.module
    module.triple = llvm.get_default_triple()

    if COMPILER_DEBUG:
        with open("debug/ir.ll", "w") as f:
            f.write(str(module))