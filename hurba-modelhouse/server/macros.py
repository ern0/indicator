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


	def napirend(self,number):

		if number == 700: print("ebreszto")
		if number == 730: print("nyomas az iskolaba")
		if number == 800: print("becsengettek")
		if number == 2000: print("nyomas az agyba")
		if number == 0: print("ejfel")


	def harang(self,number,minute):
		if 1200 <= number and number <= 1203: 
			if minute % 2 == 0: print("bim")
			else: print("bam")


	def kakukk(self,hour,minute):
		if minute == 0:
			if hour in [7,8,9,10,11,13,14,15,16,17,18,19,20]:
				print("kakukk")		


	def clock(self,stamp):
		(hour,minute) = stamp.split(":")
		hour = int(hour)
		minute = int(minute)
		number = (hour * 100) + minute

		self.napirend(number)
		self.harang(number,minute)
		self.kakukk(hour,minute)


	def one(self):

		self.api.reset()
		for i in range(0,5):
			self.api.light(i * 8,["0e0","0e0","0e0"])
			self.api.sleep(0.5)
			self.api.reset()


	def color(self,color):
		self.api.light(self.konyha,color)
		

	def red(self):
		self.api.light(self.konyha,self.piros)
		self.api.bgplay("kwah")


	def yellow(self):
		self.api.light(self.konyha,"770")


	def green(self):
		self.api.light(self.konyha,"070")
