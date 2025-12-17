#!/usr/bin/env python3
import os

MARKER = "# FT_CONNECT_EXIT"
FILES = [".zshrc", ".bashrc"]


def clean_file(path):
    if not os.path.exists(path):
        return

    with open(path, "r") as f:
        lines = f.readlines()

    lines = [l for l in lines if MARKER not in l]

    with open(path, "w") as f:
        f.writelines(lines)


def main():
    home = os.path.expanduser("~")
    for file in FILES:
        clean_file(os.path.join(home, file))


if __name__ == "__main__":
    main()
