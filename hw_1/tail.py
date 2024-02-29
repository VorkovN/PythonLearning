import argparse
import sys


def tail(files=None):
    if not files:
        lines = sys.stdin.readlines()
        print(''.join(lines[-17:]), end='')
        print()
    else:
        for file in files:
            print(f"==> {file} <==")
            with open(file, 'r') as f:
                lines = f.readlines()
                print(''.join(lines[-10:]), end='')
                print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility similar to tail -b a")
    parser.add_argument("input_file", nargs="*")
    args = parser.parse_args()

    tail(args.input_file)