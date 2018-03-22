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
	# count number of running instances of a command

	def check(self):

		command = self.config["parm"]

		output = os.popen(
			"ps -e -o ucomm"
			" | cut -d' ' -f1"
			" | grep '^" + command + "$'"
			" | wc -l"
		).read()

		return int(output)


class CheckCmd(indicator.Module):
	# count output lines of a custom command

	def check(self):

		command = self.config["parm"]
		output = os.popen(command + " | wc -l").read()

		return int(output)
