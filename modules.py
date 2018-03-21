
def checkPs(self,pattern):

	r = os.popen(
		"ps -ef | grep " + pattern + "| grep -v grep"
	).read()
	
	return r > 0


def tst(self,parm):
	print("[" + str(parm) + "]")
	return self.tick

