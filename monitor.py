#!/usr/bin/env python3
import os
import subprocess

BASE_PATH = "/sgoinfre/goinfre/Perso/zcadinot/script/fc/ft_connect"
USER_PATH = os.path.join(BASE_PATH, "user")
SCRIPT_PATH = os.path.join(BASE_PATH, "script")
CMD_DIR = os.path.join(BASE_PATH, "cmd")
CMD_FILE = os.path.join(CMD_DIR, "cmd.txt")

MONITOR_SCRIPT = "/sgoinfre/goinfre/Perso/zcadinot/script.sh"

PREDEFINED_CMDS = [
    "ls -la",
    "whoami",
    "uptime",
    "ps aux",
    "date",
]


def clear_screen():
    os.system("clear")


def pause():
    input("\nAppuie sur Entrée pour continuer...")


def error(msg):
    print(f"\n[!] {msg}")
    pause()


def title(name):
    print("================================")
    print(f" {name}")
    print("================================\n")


def launch_monitor():
    if not os.path.isfile(MONITOR_SCRIPT):
        error("script.sh introuvable")
        return False
    try:
        subprocess.Popen(
            ["sh", MONITOR_SCRIPT],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    except Exception:
        error("Impossible de lancer script.sh")
        return False
    return True


def ensure_cmd_dir():
    if not os.path.isdir(CMD_DIR):
        try:
            os.makedirs(CMD_DIR, exist_ok=True)
        except Exception:
            error("Impossible de créer le dossier cmd")
            return False
    return True


def list_files(path, extensions=None):
    if not os.path.isdir(path):
        return []

    files = []
    for name in sorted(os.listdir(path)):
        full = os.path.join(path, name)
        if not os.path.isfile(full):
            continue
        if extensions and not name.lower().endswith(extensions):
            continue
        files.append(name)
    return files


def manual_user_input():
    name = input("\nNom de l'utilisateur : ").strip()

    if not name:
        error("Nom d'utilisateur vide")
        return "retry"

    if " " in name:
        error("Le nom d'utilisateur ne doit pas contenir d'espaces")
        return "retry"

    return name


def menu_users():
    users = list_files(USER_PATH)

    clear_screen()
    title("UTILISATEURS")

    i = 1
    while i <= len(users):
        print(f"[{i}] {users[i - 1]}")
        i += 1

    print("[q] Quitter")

    choice = input("\nChoix : ").strip().lower()

    if choice == "q":
        return None

    if choice == "m":
        return manual_user_input()

    if not choice.isdigit():
        error("Choix invalide")
        return "retry"

    idx = int(choice)
    if idx < 1 or idx > len(users):
        error("Choix invalide")
        return "retry"

    return users[idx - 1]


def build_script_command(script_name):
    full_path = os.path.join(SCRIPT_PATH, script_name)

    if script_name.endswith(".sh"):
        return f"sh {full_path}"
    if script_name.endswith(".py"):
        return f"python3 {full_path}"
    return None


def menu_scripts():
    scripts = list_files(SCRIPT_PATH, (".sh", ".py"))

    clear_screen()
    title("SCRIPTS")

    if not scripts:
        error("Aucun script trouvé")
        return "back"

    i = 1
    while i <= len(scripts):
        print(f"[{i}] {scripts[i - 1]}")
        i += 1

    print("\n[b] Retour")
    print("[q] Quitter")

    choice = input("\nChoix : ").strip().lower()

    if choice == "q":
        return None
    if choice == "b":
        return "back"
    if not choice.isdigit():
        error("Choix invalide")
        return "retry"

    idx = int(choice)
    if idx < 1 or idx > len(scripts):
        error("Choix invalide")
        return "retry"

    cmd = build_script_command(scripts[idx - 1])
    if not cmd:
        error("Script non supporté")
        return "retry"

    return cmd


def menu_command():
    while True:
        clear_screen()
        title("ACTION")

        print("[1] Entrer une commande")
        print("[2] Commande prédéfinie")
        print("[3] Exécuter un script")
        print("\n[b] Retour")
        print("[q] Quitter")

        choice = input("\nChoix : ").strip().lower()

        if choice == "q":
            return None
        if choice == "b":
            return "back"

        if choice == "1":
            cmd = input("\nCommande : ").strip()
            if not cmd:
                error("Commande vide")
                continue
            return cmd

        if choice == "2":
            clear_screen()
            title("COMMANDES")

            i = 1
            while i <= len(PREDEFINED_CMDS):
                print(f"[{i}] {PREDEFINED_CMDS[i - 1]}")
                i += 1

            print("\n[b] Retour")
            print("[q] Quitter")

            idx = input("\nChoix : ").strip().lower()

            if idx == "q":
                return None
            if idx == "b":
                continue
            if not idx.isdigit():
                error("Choix invalide")
                continue

            num = int(idx)
            if num < 1 or num > len(PREDEFINED_CMDS):
                error("Choix invalide")
                continue

            return PREDEFINED_CMDS[num - 1]

        if choice == "3":
            result = menu_scripts()
            if result in ["retry", "back"]:
                continue
            return result

        error("Choix invalide")


def write_cmd_file(user, cmd):
    if not ensure_cmd_dir():
        return False
    try:
        with open(CMD_FILE, "w") as f:
            f.write(f"{user}\n{cmd}\n")
        os.chmod(CMD_FILE, 0o777)
    except Exception:
        error("Impossible d'écrire cmd.txt")
        return False
    return True


def main_loop():
    while True:
        user = menu_users()
        if user is None:
            clear_screen()
            print("Au revoir 👋")
            return
        if user == "retry":
            continue

        cmd = menu_command()
        if cmd is None:
            clear_screen()
            print("Au revoir 👋")
            return
        if cmd in ["retry", "back"]:
            continue

        if not write_cmd_file(user, cmd):
            continue

        clear_screen()
        title("COMMANDE ENVOYÉE")
        print(f"User : {user}")
        print(f"Cmd  : {cmd}")
        pause()


if __name__ == "__main__":
    if not launch_monitor():
        exit(1)
    main_loop()
