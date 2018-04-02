#!/usr/bin/env python3

import sys
sys.dont_write_bytecode = True

import importmodule


class ExecuteModule:


	def main(self):

		self.about()
		self.executeModule()
		self.displayResult()


	def about(self):

		if len(sys.argv) == 4: return

		print("xmod - execute module")
		print("usage:")
		print(" xmod path/to/ModulePack.py ModuleClassName parameter")

		quit()


	def executeModule(self):

		self.pack = sys.argv[1]
		self.module = sys.argv[2]	
		try: self.parm = int(sys.argv[3])
		except ValueError: self.parm = sys.argv[3]

		self.imported = importmodule.importmodule(self.pack)
		mod = eval( "self.imported." + self.module + "()" )

		try:
			hasInit = False
			dummy = mod.init
			hasInit = True
		except:
			pass

		mod.result = 0
		mod.parameter = self.parm

		if hasInit: mod.init()
		mod.check()

		self.result = mod.getResult()


	def displayResult(self):

		print(
			"pack=" + self.pack 
			+ " module=" + self.module
			+ " parm=" + str(self.parm)
			+ "\nresult=" + str(self.result)
		)


if __name__ == "__main__":

	(ExecuteModule()).main()