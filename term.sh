#!/bin/bash
# --- write_cmd.sh ---
# Demande un utilisateur + une commande, puis écrit dans cmd.txt

CMD_FILE="/sgoinfre/goinfre/Perso/zcadinot/ft_connect/cmd/cmd.txt"

# S'assurer que le dossier existe
mkdir -p "$(dirname "$CMD_FILE")"

# Lire le nom d'utilisateur
read -rp "Nom d'utilisateur (ou 'all' pour tous) : " USERNAME

# Lire la commande
read -rp "Commande à exécuter : " COMMAND

# Écrire dans le fichier
{
    echo "$USERNAME"
    echo "$COMMAND"
} > "$CMD_FILE"

chmod 666 "$CMD_FILE"

echo "✅ Commande enregistrée dans : $CMD_FILE"
echo "-----------------------------------------"
cat "$CMD_FILE"

