listen = 9096
forward = "http://localhost:9095"

check = [

	{ 
		"token": "make",
		#"module": modules.CheckPs,
		"parm": "make",
		"freq": 1,
	},

]
