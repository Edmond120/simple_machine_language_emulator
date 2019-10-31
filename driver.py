import sys

import emulator

def main(argv):
	memory_file_path   = 'memory'
	register_file_path = 'registers'
	start_address      = '0x0'

	settings = {
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
	}

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
		elif arg == 'no_clear':
			settings['clear'     ] = False
		else:
			print('unknown argument:',arg,file=sys.stderr)
			exit(1)

	with open(memory_file_path,'r') as memory_file, open(register_file_path,'r') as register_file:
		return emulator.emulate(memory_file,register_file,start_address,settings)

if __name__ == '__main__':
	exit(main(sys.argv[1:]))
