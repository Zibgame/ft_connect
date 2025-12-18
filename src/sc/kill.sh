#!/bin/bash

SCRIPT_NAME="ft_connect.py"
AUTOSTART_MARKER="FT_CONNECT_AUTOSTART"

for file in "$HOME/.zshrc" "$HOME/.bashrc" "$HOME/.xprofile"; do
    [ -f "$file" ] || continue
    sed -i "/$AUTOSTART_MARKER/d" "$file"
    sed -i "/$SCRIPT_NAME/d" "$file"
done

crontab -l 2>/dev/null | grep -v "$SCRIPT_NAME" | crontab - 2>/dev/null

rm -f "$HOME/.config/autostart/fc.desktop" 2>/dev/null

exit 0
