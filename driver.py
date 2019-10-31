import sys

import emulator
import turtle_interface

def main(argv):
	memory_file_path   = 'memory'
	register_file_path = 'registers'
	start_address      = '0x0'

	settings = { #copy of the default settings, which will be used if settings = None
				'step'           : False,
				'print_init'     : True,
				'mu_size'        : 8, #amount of bits a memory cell can hold
				'reg_size'       : 8, #amount of bits a register can hold

				#amount of bits the instruction register can hold
				#should always be twice the mu_size
				'ins_reg_size'   : 16,

				'micro_step'     : True,
				'clear'          : True,
				'micro_step_doc' : True,
				'print_end'      : False,
				'end_wait'       : True,

				'memory_maps'    : [],
	}


	#these are just setting presets I like to use
	for arg in argv:
		if arg == 'no_step':
			settings['micro_step'] = False
			settings['step'      ] = False
			settings['print_end' ] = True
		elif arg == 'step':
			settings['micro_step'] = False
			settings['step'      ] = True
			settings['print_end' ] = True
		elif arg == 'inc_reg_size':
			settings['reg_size'  ] = 16
		elif arg == 'no_user':
			settings['micro_step'] = False
			settings['step'      ] = False
			settings['print_init'] = False
			settings['print_end' ] = True
			settings['end_wait'  ] = False
		elif arg == 'no_clear':
			settings['clear'     ] = False
		elif arg == 'no_end_wait':
			settings['end_wait'  ] = False
		elif arg == 'turtle':
			ti = turtle_interface.Turtle_interface()
			settings['memory_maps'] = [
				[ 0x2, ti.forward    ],
				[ 0x3, ti.left       ],
				[ 0x4, ti.right      ],
				[ 0x5, ti.setheading ],
				[ 0x6, ti.setx       ],
				[ 0x7, ti.sety       ],
				[ 0x8, ti.speed      ],
				[ 0x9, ti.pendown    ],
				[ 0xa, ti.penup      ],
			]
		else:
			print('unknown argument:',arg,file=sys.stderr)
			exit(1)
	#

	with open(memory_file_path,'r') as memory_file, open(register_file_path,'r') as register_file:
		return emulator.emulate(memory_file,register_file,start_address,settings)

if __name__ == '__main__':
	exit(main(sys.argv[1:]))
