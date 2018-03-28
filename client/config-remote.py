import module.Test

listen = 9096
forward = "http://localhost:9095"

check = [

	{ 
		"token": "true",
		"module": module.Test.Echo,
		"parm": 1,
		"freq": 1,
	},
	{ 
		"token": "false",
		"module": module.Test.Echo,
		"parm": 0,
		"freq": 1,
	},
	{ 
		"token": "zulu",
		"module": module.Test.Zero,
		"freq": 1,
	},
	{ 
		"token": "inc",
		"module": module.Test.Inc,
		"parm": 5,
		"freq": 1,
	},

]
