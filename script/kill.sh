#!/bin/bash

MASTER_USER="zcadinot"
SCRIPT_NAME="ft_connect.py"

if [ "$(whoami)" != "$MASTER_USER" ]; then
    echo "[!] Accès refusé"
    exit 1
fi

pids=$(pgrep -f "$SCRIPT_NAME")

if [ -z "$pids" ]; then
    echo "[i] Aucun ft_connect.py en cours"
else
    echo "[i] Arrêt de ft_connect.py"
    kill $pids 2>/dev/null
    sleep 1

    pids=$(pgrep -f "$SCRIPT_NAME")
    if [ -n "$pids" ]; then
        echo "[!] Kill forcé"
        kill -9 $pids 2>/dev/null
    fi

    echo "[✓] ft_connect arrêté"
fi

echo "[✓] Extinction complète"
