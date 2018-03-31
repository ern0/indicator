import example.ExampleModule

listen = 9095
device = "/dev/ttyUSB0"


check = [

	{ 
		"token": "flipflop",
		"module": example.ExampleModule.FlipFlop,
		"parm": 0,
		"freq": 2,
	},

	{ 
		"token": "flopflip",
		"module": example.ExampleModule.FlipFlop,
		"parm": 1,
		"freq": 2,
		"phase": 1,
	},

]


show = [

	{
		"slot": 0,
		"token": "flipflop",
		"colors": [ "000", "f00" ],
	},

	{
		"slot": 1,
		"token": "flopflip",
		"colors": [ "000", "ff0" ],
	}
	
]
