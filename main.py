#!/usr/bin/env python3
import os.path
from argparse import ArgumentParser, Namespace

from pycparser import parse_file
from pycparser.c_ast import FileAST, FuncDef, NodeVisitor
from pycparser.plyparser import ParseError


class Compiler(NodeVisitor):
    def __init__(self):
        self.functions: list[FuncDef] = []

    def visit_FileAST(self, node: FileAST):
        for child in node:
            if type(child) == FuncDef:
                self.functions.append(child)


def main(args: Namespace) -> int:
    if os.path.isfile(args.input) == False:
        print(f"File {args.input} does not exist")
        return 1

    ast: FileAST = parse_file(args.input, use_cpp=True)
    compiler = Compiler()
    compiler.visit(ast)
    return 0


if __name__ == "__main__":
    parser = ArgumentParser(prog="CC80", description="C to Z80 ASM compiler")
    parser.add_argument("input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file", default="out.asm")

    exit(main(parser.parse_args()))
