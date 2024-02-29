import argparse
import sys


def nl(input_file=None):
    if input_file:
        with open(input_file, 'r') as file:
            lines = file.readlines()
    else:
        lines = sys.stdin.readlines()

    for i, line in enumerate(lines, start=1):
        print(f"     {i}  {line.strip()}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility similar to nl -b a")
    parser.add_argument("input_file", nargs="?")
    args = parser.parse_args()

    nl(args.input_file)