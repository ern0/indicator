
def init(light):
	light.lum(30)


def one(light):

	for i in range(0,5):
		light.pos(i * 8)
		light.hex(["0e0","0e0","0e0"])
		light.send()
		light.sleep(0.5)
		light.reset()
