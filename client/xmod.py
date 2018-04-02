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
		print(" xmod path/to/ModulePack.py ModuleClassName parm")

		quit()


	def executeModule(self):

		self.pack = sys.argv[1]
		self.module = sys.argv[2]	
		try: self.parm = int(sys.argv[3])
		except ValueError: self.parm = sys.argv[3]

		self.imported = importmodule.importmodule(self.pack)
		mod = eval( "self.imported." + self.module + "()" )

		try:
			mod.init(self.parm)
		except TypeError:
			mod.init()
		
		try:
			mod.check(self.parm)
		except TypeError:
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