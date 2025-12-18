import tkinter as tk
import sys

GIF = "/sgoinfre/goinfre/Perso/zcadinot/script/fc/ft_connect/src/mp4/rick.mp4"

def load_frames(path):
    frames = []
    index = 0

    try:
        while True:
            frames.append(tk.PhotoImage(file=path, format=f"gif -index {index}"))
            index += 1
    except tk.TclError:
        pass

    if not frames:
        raise RuntimeError("GIF invalide")

    return frames

def play(label, frames, index):
    label.config(image=frames[index])
    label.after(50, play, label, frames, (index + 1) % len(frames))

def main():
    try:
        root = tk.Tk()
        root.attributes("-fullscreen", True)
        root.configure(bg="black")

        frames = load_frames(GIF)

        label = tk.Label(root, bg="black")
        label.pack(expand=True)

        root.bind("<Escape>", lambda e: root.destroy())

        play(label, frames, 0)
        root.mainloop()
    except Exception as e:
        print(f"Erreur : {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()
