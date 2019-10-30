import sys

import emulator

def main(argv):
	memory_file_path   = 'memory'
	register_file_path = 'registers'
	start_address      = '0x0'

	step = False
	print_init = True
	memory_size_bits = 8

	settings = {
				'step'           : True,
				'print_init'     : True,
				'mu_size'        : 8, #amount of bits a memory cell can hold
				'reg_size'       : 16, #amount of bits a register can hold
				'micro_step'     : True,
				'clear'          : True,
				'micro_step_doc' : True,
	}

	with open(memory_file_path,'r') as memory_file, open(register_file_path,'r') as register_file:
		return emulator.emulate(memory_file,register_file,start_address,settings)

if __name__ == '__main__':
	exit(main(sys.argv))
