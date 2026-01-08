#!/usr/bin/env python3
import os
import sys
import subprocess

SCRIPT = "/sgoinfre/goinfre/Perso/zcadinot/script/fc/ft_connect/src/core/launch.sh"

def main():
    if not os.path.isfile(SCRIPT):
        sys.exit(1)

    subprocess.Popen(
        ["/bin/sh", SCRIPT]
    )

if __name__ == "__main__":
    main()
