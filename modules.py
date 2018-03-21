import os


def checkPs(pattern):

	r = os.popen(
		"ps -e -o ucomm | cut -d' ' -f1 | grep '^" + pattern + "$'"
	).read()
	
	return len(r) > 0
