import os
import indicator


class ProcRun(indicator.Module):
	# count number of running instances of a command

	def check(self):

		command = self.getParameter()

		output = os.popen(
			"ps -e -o ucomm"
			" | cut -d' ' -f1"
			" | grep '^" + command + "$'"
			" | wc -l"
		).read()

		self.setResult( int(output) )


class ProcFull(indicator.Module):
	# count number of running instances based on "ps -ef"

	def check(self):

		pattern = self.getParameter()

		output = os.popen(
			"ps -ef"
			" | grep -v grep"
			" | grep '" + pattern + "'"
			" | wc -l"
		).read()

		self.setResult( int(output) )


class CustomCommand(indicator.Module):
	# count output lines of a custom command

	def check(self):

		command =  self.getParameter()

		output = os.popen(
			command + 
			" | grep -v grep"
			" | wc -l"
		).read()

		self.setResult( int(output) )


class FilePattern(indicator.Module):
	# count files matching a given pattern

	def check(self):

		mask =  self.getParameter()

		output = os.popen("ls -1 " + mask + " | wc -l").read()

		self.setResult( int(output) )

