import example.ExampleModulePack as e

listen = 9095


check = [

	{ 
		"token": "flipflop",
		"module": e.FlipFlop,
		"parm": 0,
		"freq": 2,
	},

	{ 
		"token": "flopflip",
		"module": e.FlipFlop,
		"parm": 1,
		"freq": 2,
		"phase": 1,
	},

	{ 
		"token": "ff",
		"module": e.FlipFlop,
		"parm": 1,
		"freq": 5,
		"phase": 3,
	},

]


show = [

	{
		"slot": 0,
		"token": "flipflop",
		"colors": [ "000", "f00" ],
	},

	{
		"slot": 2,
		"token": "flopflip",
		"colors": [ "000", "ff0" ],
	},

	{
		"slot": 6,
		"token": "remote",
		"colors": [ "000", "33f", "0ff" ],
	},

	{
		"slot": 7,
		"token": "ff",
		"colors": [ "000", "fff" ],
	}
	
]
