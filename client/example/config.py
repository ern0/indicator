# This is the example configuration for Indicator


# The configuration must import the modules used.
# This line refers to "example/Example.py"
import example.ExampleModule


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
		"module": example.ExampleModule.Echo,
		"parm": 1,
		"freq": 1,
	},
	{ 
		"token": "false",
		"module": example.ExampleModule.Echo,
		"parm": 0,
		"freq": 1,
	},
	{ 
		"token": "zulu",
		"module": example.ExampleModule.Zero,
		"freq": 1,
	},
	{ 
		"token": "inc",
		"module": example.ExampleModule.Inc,
		"parm": 5,
		"freq": 1,
	},
]
