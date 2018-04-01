import example.ExampleModule

forward = [
	"http://localhost:9095"
]

check = [

	{ 
		"token": "remote",
		"module": example.ExampleModule.FlipFlop,
		"parm": 0,
		"freq": 1,
	},

]
