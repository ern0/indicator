listen = 9095
xxx_device = "/dev/ttyUSB0"

check = [

	{ 
		"token": "ld",
		#"module": modules.CheckPs,
		"parm": "make",
		"freq": 1,
	},

]

show = [
	{
		"slot": 0,
		"token": "make",
		"colors": [ "000", "f00" ],
	},

	{
		"slot": 0,
		"token": "make",
		"colors": [ "000", "f00" ],
	}
	
]
