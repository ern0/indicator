#/bin/bash
clear

server/server.py
exit

if [ "$TERM" != "screen" ]; then
	tmux new -d -s server "server/server.py ; sleep 9999"
	tmux split-window "bash ; tmux kill-session -t server"
	tmux a
	exit 0
fi

curl localhost:8080/light/one
