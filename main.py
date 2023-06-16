#!/usr/bin/env python3
import os.path
from argparse import ArgumentParser, Namespace
from io import TextIOWrapper

from pycparser import parse_file
from pycparser.c_ast import Decl, FileAST, FuncDef, NodeVisitor
from pycparser.plyparser import ParseError


class Compiler(NodeVisitor):
    def __init__(self, ast: FileAST):
        self.output: TextIOWrapper
        self.ast: FileAST = ast

        self.text: list[FuncDef] = []
        self.data: list[Decl] = []
        self.rodata: list[Decl] = []
        self.bss: list[Decl] = []
    
    def write(self, s: str):
        self.output.write(s)

    def compile(self, output: str):
        self.output = open(output, "w")
        self.write("; " + ("=" * 78) + "\n")
        self.write("; Generated by CC80. Use with Z88DK assembler.\n")
        self.write("; " + ("=" * 78) + "\n")

        # Note: does not actually compile anything. We want to gather all the
        # top-level stuff first so we can organize them in the output.
        self.visit(self.ast)

        if len(self.text) > 0:
            self.write("\nSECTION text\n")
            for function in self.text:
                self.visit(function)

        if len(self.data) > 0:
            self.write("\nSECTION data\n")
            for symbol in self.data:
                self.visit(symbol)

        if len(self.rodata) > 0:
            self.write("\nSECTION rodata\n")
            for symbol in self.rodata:
                self.visit(symbol)

        if len(self.bss) > 0:
            self.write("\nSECTION bss\n")
            for symbol in self.bss:
                self.visit(symbol)

        self.output.close()

    def visit_FileAST(self, node: FileAST):
        for child in node.ext:
            match child.__class__.__name__:
                case "FuncDef":
                    self.text.append(child)
                case "Decl":
                    if child.init == None:
                        self.bss.append(child)
                    else:
                        if "const" in child.quals:
                            self.rodata.append(child)
                        else:
                            self.data.append(child)
                case _:
                    print(
                        f"Unimplemented top-level node `{child.__class__.__name__}`, generated assembly may be incorrect."
                    )

    def visit_FuncDef(self, node: FuncDef):
        pass

    def visit_Decl(self, node: Decl):
        pass


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
