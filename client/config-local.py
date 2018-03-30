listen = 9095
device = "/dev/ttyUSB0"

import example.ExampleModule
check = [

	{ 
		"token": "true",
		"module": example.ExampleModule.Echo,
		"parm": 1,
		"freq": 1,
	},
]

show = [
	{
		"slot": 0,
		"token": "true",
		"colors": [ "000", "f00" ],
	},

	{
		"slot": 0,
		"token": "make",
		"colors": [ "000", "f00" ],
	}
	
]
