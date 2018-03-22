#/bin/bash
clear

./indicator.py ; exit

if [ "$TERM" != "screen" ]; then
	tmux new -d -s indicator "./indicator.py ; sleep 9999"
	tmux split-window "bash ; tmux kill-session -t indicator"
	tmux a
	exit 0
fi
