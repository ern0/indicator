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


class ProcRun(indicator.Module):
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


class ProcFull(indicator.Module):
	# count number of running instances based on "ps -ef"

	def check(self):

		pattern = self.config["parm"]

		output = os.popen(
			"ps -ef"
			" | grep -v grep"
			" | grep '" + pattern + "'"
			" | wc -l"
		).read()

		return int(output)


class CustomCommand(indicator.Module):
	# count output lines of a custom command

	def check(self):

		command = self.config["parm"]
		output = os.popen(
			command + 
			" | grep -v grep"
			" | wc -l"
		).read()

		return int(output)


class FilePattern(indicator.Module):
	# count files matching a given pattern

	def check(self):

		mask = self.config["parm"]
		output = os.popen("ls -1 " + mask + " | wc -l").read()

		return int(output)

