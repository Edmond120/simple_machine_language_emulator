def emulate(memory_file,register_file,start_address,step=False):
	memory    = load_data(memory_file)
	registers = load_data(register_file)
	program_counter = int(start_address,16)
	instruction_register = memory[program_counter] * 16 + memory[program_counter + 1]
	settings = {'step':step}
	run_emulator(memory,registers,program_counter,instruction_register,settings)

def run_emulator(memory,registers,program_counter,instruction_register,settings):
	pass

def load_data(data_file):
	data={}
	for line in data_file:
		address, info = line.split(" ")
		data[int(address,16)] = int(data,16)
	return data
