import modules

cfg = [

	{
		"slot": 0,
		"func": modules.tst,
		"parm": True,
		"freq": 4,
		"phase": 0,
		"low": "000",
		"rise": "444",
		"high": "f00",
		"fall": "500",
		"sust": 3,
	},

	{
		"slot": 0,
		"func": modules.tst,
		"parm": False,
		"freq": 4,
		"phase": 2,
		"low": [ 0,0,0 ],
		"rise": [ 44,44,44 ],
		"high": [ 255,0,0 ],
		"fall": [ 44,44,44 ],
		"sust": 3,
	}

]