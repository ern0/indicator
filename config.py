import modules


cfg = [

	{
		"slot": 0,
		"func": modules.checkPs,
		"parm": "cat",
		"freq": 4,
		"low": "000",
		"rise": "444",
		"high": "f00",
		"fall": "500",
		"sust": 3,
	},

	{
		"slot": 0,
		"func": modules.checkPs,
		"parm": "tail",
		"freq": 4,
		"phase": 2,
		"low": "000",
		"rise": "444",
		"high": "f00",
		"fall": "444",
		"sust": 3,
	},

	{
		"slot": 1,
		"func": modules.checkPs,
		"parm": "cat",
		"freq": 1,
		"low": "000",
		"rise": "444",
		"high": "f00",
		"fall": "444",
		"sust": 3,
	},

	{
		"slot": 2,
		"func": modules.checkPs,
		"parm": "tail",
		"freq": 1,
		"low": "000",
		"rise": "444",
		"high": "f00",
		"fall": "444",
		"sust": 3,
	},

]