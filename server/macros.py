def init(self):

	self.reset()
	self.lum(100)

	self.konyha = [22,25,39]
	self.piros = "f00"

	self.fgplay("kwah")

	self.light([0,7,32,38],["00f","00f"])


def reset(self):
	self.reset()


def one(self):

	self.reset()
	for i in range(0,5):
		self.light(i * 8,["0e0","0e0","0e0"])
		self.sleep(0.5)
		self.reset()


def red(self):
	self.light(self.konyha,self.piros)
	self.bgplay("kwah")


def yellow(self):
	self.light(self.konyha,"770")


def green(self):
	self.light(self.konyha,"070")