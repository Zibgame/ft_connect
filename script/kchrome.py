import os
import platform

def close_all_chrome():
    system = platform.system()

    if system == "Linux":
        os.system("pkill -f chrome")
    elif system == "Darwin":
        os.system("pkill -f 'Google Chrome'")
    elif system == "Windows":
        os.system("taskkill /IM chrome.exe /F")

if __name__ == "__main__":
    close_all_chrome()
