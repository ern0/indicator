

def init(api):
	api.lum(100)
	api.pos(2)
	api.hex("fff")
	api.send()
	api.fgplay("261")
	api.pos(2)
	api.hex("000")


def reset(api):
	api.reset()


def one(api):

	for i in range(0,5):
		api.pos(i * 8)
		api.hex(["0e0","0e0","0e0"])
		api.sleep(0.5)
		api.reset()


def red(api):
	api.pos(22)
	api.hex("700")
	api.bgplay("kwah")


def yellow(api):
	api.pos(22)
	api.hex("770")

def green(api):
	api.pos(22)
	api.hex("070")