import example.ExampleModulePack as e

listen = 9096

forward = [
	"http://localhost:9095"
]

check = [

	{ 
		"token": "remote",
		"module": e.FlipFlop,
		"parm": 0,
		"freq": 3,
	},

]
