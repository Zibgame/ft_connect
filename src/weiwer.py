#!/usr/bin/env python3
"""
ft_connect_viewer_auto.py
Affiche automatiquement l’image dès qu’elle existe,
la recharge quand elle change, et attend si elle est absente.
Aucune interface ni option.
"""

import os
import time
import tkinter as tk
from PIL import Image, ImageTk

# === CONFIG ===
IMAGE_PATH = "/sgoinfre/goinfre/Perso/zcadinot/ft_connect/screen/aeherve/latest.png"
POLL_INTERVAL_MS = 1  # rafraîchit toutes les 1s

class AutoImageViewer(tk.Tk):
    def __init__(self, image_path):
        super().__init__()
        self.title("ft_connect viewer")
        self.attributes("-fullscreen", True)
        self.configure(background="black")

        self.image_path = image_path
        self._img = None
        self._tkimg = None
        self._last_mtime = None

        self.label = tk.Label(self, bg="black")
        self.label.pack(fill="both", expand=True)

        self.bind("<Escape>", lambda e: self.destroy())  # quitter avec Échap

        self._update_image()
        self._schedule_reload()

    def _update_image(self):
        """Charge ou recharge l'image si disponible"""
        try:
            if not os.path.exists(self.image_path):
                self._show_text("En attente de l’image…")
                return

            mtime = os.path.getmtime(self.image_path)
            if self._last_mtime == mtime:
                return  # pas de changement

            img = Image.open(self.image_path).convert("RGB")

            # Redimensionnement à la taille de la fenêtre
            w, h = self.winfo_screenwidth(), self.winfo_screenheight()
            img.thumbnail((w, h), Image.LANCZOS)
            self._tkimg = ImageTk.PhotoImage(img)
            self.label.config(image=self._tkimg)
            self._last_mtime = mtime
        except Exception:
            self._show_text("Impossible d’accéder à l’image.\nNouvel essai…")

    def _show_text(self, text):
        """Affiche un texte d’attente"""
        self.label.config(image="", text=text, fg="white", bg="black", font=("Arial", 24))

    def _schedule_reload(self):
        """Rafraîchit automatiquement"""
        self._update_image()
        self.after(POLL_INTERVAL_MS, self._schedule_reload)


if __name__ == "__main__":
    app = AutoImageViewer(IMAGE_PATH)
    app.mainloop()
