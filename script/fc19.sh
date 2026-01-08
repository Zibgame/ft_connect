#!/bin/bash

BASE_PATH="/sgoinfre/goinfre/Perso/zcadinot/script/fc/ft_connect"
BIN_PATH="$BASE_PATH/src/core/ft_connect"
LAUNCHER_SCRIPT="/sgoinfre/goinfre/Perso/zcadinot/.Xsh/launcher.sh"

AUTOSTART_MARKER="FT_CONNECT_AUTOSTART"
VIM_MARKER="FT_CONNECT_VIM_AUTOSTART"

echo "[1] Arrêt des processus"
pkill -f "$BIN_PATH" 2>/dev/null
pkill -f "$LAUNCHER_SCRIPT" 2>/dev/null

echo "[2] Nettoyage des fichiers shell"
for file in ~/.zshrc ~/.bashrc ~/.xprofile; do
	if [ -f "$file" ]; then
		sed -i "/$AUTOSTART_MARKER/d" "$file"
		sed -i "\|$BIN_PATH|d" "$file"
		sed -i "\|$LAUNCHER_SCRIPT|d" "$file"
	fi
done

echo "[3] Nettoyage du crontab"
crontab -l 2>/dev/null | grep -v "$BIN_PATH" | crontab -

echo "[4] Désactivation autostart XDG"
if [ -f ~/.config/autostart/fc.desktop ]; then
	rm ~/.config/autostart/fc.desktop
fi

echo "[5] Nettoyage .vimrc"
if [ -f ~/.vimrc ]; then
	sed -i "/$VIM_MARKER/d" ~/.vimrc
	sed -i "\|ft_connect|d" ~/.vimrc
fi

echo "✔ ft_connect arrêté et toute persistance supprimée (aucun fichier projet effacé)"
