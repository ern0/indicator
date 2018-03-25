import modules


cfg = [


	# compiler 
	
	{ 
		"slot": 7 +32,
		"module": modules.CheckPs,
		"parm": "make",
		"freq": 1,
		"colors": ["006","ff0"]
	},

	{ 
		"slot": 6 +32,
		"module": modules.CheckPs,
		"parm": "gcc",
		"freq": 1,
		"colors": ["006","3f3"]
	},

	{ 
		"slot": 5 +32,
		"module": modules.CheckPs,
		"parm": "ld",
		"freq": 1,
		"colors": ["006","f33"]
	},


]
