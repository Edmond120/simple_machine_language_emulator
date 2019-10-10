import emulator

def main():
	memory_file_path   = 'memory'
	register_file_path = 'registers'
	start_address      = '0x0'
	with open(memory_file_path,'r') as memory_file, open(register_file_path,'r') as register_file:
		emulator.emulate(memory_file,register_file,start_address)

if __name__ == '__main__':
	main()
