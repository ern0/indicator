# This is the example configuration for Indicator


# The configuration must import the modules used.
# This line refers to "example/Example.py"
import example.ExampleModulePack


# Listen port for receiving data from other hosts 
listen = 9096


# List of URLs to send collected data
forward = [
	"http://localhost:9095"
]


# List of local data collectors
check = [
	{ 
		"token": "true",
		"module": example.ExampleModulePack.Echo,
		"parm": 1,
		"freq": 1,
	},
	{ 
		"token": "false",
		"module": example.ExampleModulePack.Echo,
		"parm": 0,
		"freq": 1,
	},
	{ 
		"token": "zulu",
		"module": example.ExampleModulePack.Zero,
		"freq": 1,
	},
	{ 
		"token": "inc",
		"module": example.ExampleModulePack.Increment,
		"parm": 5,
		"freq": 1,
	},
]
