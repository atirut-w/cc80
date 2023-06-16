#!/usr/bin/env python3
import os.path
from argparse import ArgumentParser, Namespace
from io import TextIOWrapper

from pycparser import parse_file
from pycparser.c_ast import FileAST, FuncDef, NodeVisitor
from pycparser.plyparser import ParseError


class Compiler(NodeVisitor):
    def __init__(self, ast: FileAST):
        self.output: TextIOWrapper
        self.functions: list[FuncDef] = []

    def compile(self, output: str):
        self.output = open(output, "w")
        with self.output as f:
            f.write("; " + ("=" * 78) + "\n")
            f.write("; Generated by CC80\n")
            f.write("; " + ("=" * 78) + "\n\n")

        self.visit(self.ast)


def main(args: Namespace) -> int:
    if os.path.isfile(args.input) == False:
        print(f"File {args.input} does not exist")
        return 1

    ast: FileAST = parse_file(args.input, use_cpp=True)
    compiler = Compiler(ast)
    compiler.compile(args.output)
    return 0


if __name__ == "__main__":
    parser = ArgumentParser(prog="CC80", description="C to Z80 ASM compiler")
    parser.add_argument("input", help="Input file")
    parser.add_argument("-o", "--output", help="Output file", default="out.asm")

    exit(main(parser.parse_args()))
