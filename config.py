import modules


cfg = [

	{
		"slot": 0,
		"module": modules.CheckPs,
		"parm": "cat",
		"freq": 4,
		"colors": ["100","f00"]
	},

	{
		"slot": 0,
		"module": modules.CheckPs,
		"parm": "tail",
		"freq": 4,
		"phase": 2,
		"colors": ["001","00f"]
	},

	{
		"slot": 1,
		"module": modules.CheckPs,
		"parm": "cat",
		"freq": 1,
		"colors": ["100","f00"]
	},

	{
		"slot": 2,
		"module": modules.CheckPs,
		"parm": "tail",
		"freq": 1,
		"colors": ["001","00f"]
	},

]