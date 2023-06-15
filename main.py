#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace


def main(args: Namespace) -> int:
    try:
        with open(args.input, "r") as f:
            print(f.read())
    except FileNotFoundError:
        print(f"File '{args.input}' not found")
        return 1
    return 0


if __name__ == "__main__":
    parser = ArgumentParser(prog="CC80", description="C to Z80 ASM compiler")
    parser.add_argument("input", help="Input file")

    exit(main(parser.parse_args()))
