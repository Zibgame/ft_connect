import os
import platform

def close_all_vscode(system):
    if system == "Linux":
        os.system("pkill -f code")
    elif system == "Darwin":
        os.system("pkill -f 'Visual Studio Code'")
    elif system == "Windows":
        os.system("taskkill /IM Code.exe /F")

def open_vim():
    os.system("vim")

def close_vscode_and_open_vim():
    system = platform.system()
    close_all_vscode(system)
    open_vim()

if __name__ == "__main__":
    close_vscode_and_open_vim()