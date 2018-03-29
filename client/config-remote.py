# This is the configuration for example
import example.ExampleModule

forward = [
	"http://localhost:9095",
	"http://localhost:9095"
]

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
