import sys
import os

import simple_machine_language as sml

def clear():
	if os.name == 'nt':
		os.system('cls')
	elif os.name == 'posix':
		os.system('clear')
	else:
		print('clearing failed')

def emulate(memory_file,register_file,start_address,settings):
	memory= load_data(memory_file)
	memory['data_type'] = 'memory'
	registers = load_data(register_file)
	registers['data_type'] = 'registers'
	program_counter = int(start_address,16)
	instruction_register = 0
	return run_emulator(memory,registers,program_counter,instruction_register,settings)

def run_emulator(memory,registers,program_counter,instruction_register,settings):
	def step(condition,prompt=''):
		if not condition:
			return
		if settings['clear']:
			clear()
		show_state(memory,registers,program_counter,instruction_register,settings)
		input(prompt)

	def decode_step(condition,instruction,operand_bytes,prompt=''):
		if not condition:
			return
		if settings['clear']:
			clear()
		show_state(memory,registers,program_counter,instruction_register,settings)
		print('decoded instruction: ', hex(instruction))
		print('decoded operand    : ', *list(map(hex,operand_bytes)))
		print()
		print('operation name     : ', sml.operation_map[instruction].__name__)
		if settings['micro_step_doc']:
			print('operation documentation:')
			print('------------------------')
			print(sml.operation_map[instruction].__doc__)
		input(prompt)

	if settings['print_init']:
		print('print_init')
		step(True,'ready!...')

	while True:
		#fetch
		instruction_register = memory[program_counter] * 256 + memory[program_counter + 1]
		program_counter += 2
		#
		step(settings['micro_step'],'finished fetching, ready to decode...')
		#decode
		instruction ,operand_bytes = read_instruction(instruction_register,settings)
		operation = sml.operation_map.get(instruction)
		if operation is None:
			print('unknown operation: ', phex(instruction,settings['reg_size']//8), file=sys.stderr)
			return 1
		#
		decode_step(settings['micro_step'],instruction,operand_bytes,'finished decoding, ready to execute...')
		#execute
		msg = operation(memory,registers,settings,operand_bytes)
		if msg[0] == sml.SUCCESS:
			pass
		elif msg[0] == sml.JUMP:
			program_counter = msg[1]
		elif msg[0] == sml.ERROR:
			print('error')
			print('function name: ', operation.__name__)
			print('opcode       : ', instruction)
			print('operand      : ', operand_bytes)
			print('error message: ', msg[1])
			return 1
		elif msg[0] == sml.END:
			return 0
		#
		step(settings['micro_step'],'finished executing, ready to fetch...')
		step(settings['step'] and not settings['micro_step'],'step...')

def show_state(memory,registers,program_counter,instruction_register,settings):
	print('program_counter: ' + phex(program_counter,settings['reg_size']//4))
	print('instruction_register: ' + phex(instruction_register,settings['reg_size']//4))
	print('memory:')
	print_data(memory,p=settings['mu_size']//4)
	print('registers:')
	print_data(registers,p=settings['reg_size']//4)

def read_instruction(instruction_register,settings):
	bytes = sml.break_bytes(instruction_register,settings['ins_reg_size']//4)
	return (bytes[0],bytes[1:])

def load_data(data_file):
	data={}
	for line in data_file:
		if len(line) == 0 or line[0] == '#':
			continue
		address, info = line.split(" ")
		data[int(address,16)] = int(info,16)
	return data

def phex(s,p):
	r = hex(s)
	if len(r) < 2 + p or p == 0:
		return '0x' + ('0' * (2 + p - len(r))) + r[2:]
	else:
		return r

def _data_list(data,p):
	if len(data) > 1:
		fp = max([ len(hex(key))-2 for key in data.keys() if key != 'data_type'])
	else:
		fp = 0
	return list(map(lambda x: (phex(x,fp),phex(data[x],p),),sorted([key for key in data.keys() if key != 'data_type'])))

def print_data(data, head='\t', spacing=' : ', tail='\n', p=None):
	dl = _data_list(data,p=p)
	for item in dl:
		print(head + item[0] + spacing + item[1], end=tail)
