
def init(light):
	light.lum(30)


def reset(light):
	light.reset()


def one(light):

	for i in range(0,5):
		light.pos(i * 8)
		light.hex(["0e0","0e0","0e0"])
		light.send()
		light.sleep(0.5)
		light.reset()

def red(light):
	light.pos(22)
	light.hex("700")


def yellow(light):
	light.pos(22)
	light.hex("770")

def green(light):
	light.pos(22)
	light.hex("070")