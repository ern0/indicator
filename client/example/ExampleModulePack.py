from indicator import Module


class Echo(Module):

	def check(self):  
		self.setResult(self.getParameter())


class Zero(Module):

	def check(self):
		self.setResult(0)


class One(Module):

	def init(self):
		self.setResult(1)

	def check(self):
		pass


class Increment(Module):

	def init(self):
		self.counter = self.getParameter()

	def check(self):
		self.setResult(self.counter)
		self.counter += 1


class FlipFlop(Module):

	def init(self):
		if self.getParameter() == 0:
			self.value = 0
		else:
			self.value = 1

	def check(self):
		self.setResult(self.value)
		self.value = 1 - self.value
