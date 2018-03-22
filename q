#!/bin/bash

PORT=`./detectdevice.sh "$1"`
if [ ! -z ${PORT} ]; then
	miniterm.py ${PORT} 9600 -e --exit-char 3
fi
