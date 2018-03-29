class Echo:

	def check(self,parm):  

		return parm


class Zero:

	def check(self):

		return 0


class Inc:

	def __init__(self,parm):
		self.counter = parm - 1

	def check(self):
		self.counter += 1
		return self.counter