def emulate(memory_file,register_file,start_address,settings):
	memory    = load_data(memory_file)
	registers = load_data(register_file)
	program_counter = int(start_address,16)
	instruction_register = memory[program_counter] * 16 + memory[program_counter + 1]
	run_emulator(memory,registers,program_counter,instruction_register,settings)

def run_emulator(memory,registers,program_counter,instruction_register,settings):
	if settings['print_init']:
		print("memory:")
		print_data(memory)
		print("registers:")
		print_data(registers)

def load_data(data_file):
	data={}
	for line in data_file:
		if len(line) == 0 or line[0] == '#':
			continue
		address, info = line.split(" ")
		data[int(address,16)] = int(info,16)
	return data

def print_data(data):
	print(list(map(lambda x: (hex(x),hex(data[x]),),sorted(data.keys()))))
