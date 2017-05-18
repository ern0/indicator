class Macros:


	def init(self):

		self.api.reset()
		self.api.lum(100)

		self.konyha = [22,25,39]
		self.piros = "f00"

		self.api.fgplay("kwah")

		self.api.light([0,7,32,38],["00f","00f"])


	def reset(self):
		self.api.reset()


	def one(self):

		self.api.reset()
		for i in range(0,5):
			self.api.light(i * 8,["0e0","0e0","0e0"])
			self.api.sleep(0.5)
			self.api.reset()


	def red(self):
		self.api.light(self.konyha,self.piros)
		self.api.bgplay("kwah")


	def yellow(self):
		self.api.light(self.konyha,"770")


	def green(self):
		self.api.light(self.konyha,"070")