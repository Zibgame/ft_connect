import os

def close_everything():
    os.system("loginctl terminate-user $USER")

if __name__ == "__main__":
    close_everything()
