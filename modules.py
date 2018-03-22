import os
import indicator


# it's easy to create a simple module
class ExampleModule(indicator.Module):

	# method will be called every config["freq"] secs
	def check(self):  

		# you can use any value from the config
		parm = self.config["parm"]  

		# return None for unchanged indication
		try: result = checkStuff(parm)
		except: return None

		# calculate and return color index on result
		if (result >= 100): return 1
		else: return 0


class CheckPs(indicator.Module):
	# check "ps -e" for command name

	def check(self):

		command = self.config["parm"]

		output = os.popen(
			"ps -e -o ucomm | cut -d' ' -f1 | grep '^" + command + "$'"
		).read()

		if len(output) == 0: return 0
		else: return 1
