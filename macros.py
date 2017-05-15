
def init(light):
	light.lum(30)

def one(light):
	light.send(":228;")
	light.sleep(1)
	light.reset()
