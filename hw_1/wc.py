import argparse
import sys


def wc(files=None):
    total_lines = 0
    total_words = 0
    total_bytes = 0

    if not files:
        content = sys.stdin.read()
        lines = content.splitlines()
        words = content.split()
        total_lines += len(lines)
        total_words += len(words)
        total_bytes += len(content.encode())
        print(f"{total_lines}\t{total_words}\t{total_bytes}")
    else:
        for file in files:
            with open(file, 'r') as f:
                content = f.read()
                lines = content.splitlines()
                words = content.split()
                file_lines = len(lines)
                file_words = len(words)
                file_bytes = len(content.encode())
                total_lines += file_lines
                total_words += file_words
                total_bytes += file_bytes
                print(f"{file_lines}\t{file_words}\t{file_bytes}\t{file}")

        if len(files) > 1:
            print(f"{total_lines}\t{total_words}\t{total_bytes}\ttotal")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Utility similar to wc")
    parser.add_argument("files", nargs="*")
    args = parser.parse_args()

    wc(args.files)