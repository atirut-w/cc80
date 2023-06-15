#!/usr/bin/env python3
from argparse import ArgumentParser, Namespace


def main(args: Namespace) -> int:
    return 0


if __name__ == "__main__":
    parser = ArgumentParser()

    exit(main(parser.parse_args()))
