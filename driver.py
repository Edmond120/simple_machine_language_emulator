import emulator

def main():
	memory_file_path   = 'memory'
	register_file_path = 'registers'
	start_address      = '0x0'

	step = False
	print_init = True

	with open(memory_file_path,'r') as memory_file, open(register_file_path,'r') as register_file:
		emulator.emulate(memory_file,register_file,start_address,{'step':step,'print_init':print_init})

if __name__ == '__main__':
	main()
