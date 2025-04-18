import sys
import os

import simple_machine_language as sml

default_settings = {
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

def clear():
	if os.name == 'nt':
		os.system('cls')
	elif os.name == 'posix':
		os.system('clear')
	else:
		print('clearing failed')

def emulate(memory_file,register_file,start_address,settings):
	if settings == None:
		settings = default_settings
	memory= load_data(memory_file)
	memory['data_type'] = 'memory'
	memory['fresh'    ] = {}
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
		parse_commands(prompt)

	def decode_step(condition,instruction,operand_bytes,prompt=''):
		if not condition:
			return
		if settings['clear']:
			clear()
		show_state(memory,registers,program_counter,instruction_register,settings)
		print('decoded instruction: ', hex(instruction))
		print('decoded operand    : ', *list(map(hex,operand_bytes)))
		print()
		show_name(instruction)
		if settings['micro_step_doc']:
			show_doc(instruction)
		parse_commands(prompt)

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
			print('error',file=sys.stderr)
			print('function name: ', operation.__name__,file=sys.stderr)
			print('opcode       : ', instruction,file=sys.stderr)
			print('operand      : ', operand_bytes,file=sys.stderr)
			print('error message: ', msg[1],file=sys.stderr)
			return 1
		elif msg[0] == sml.END:
			for hook in settings['halt_hooks']:
				hook()
			if settings['print_end']:
				if settings['clear']:
					clear()
				show_state(memory,registers,program_counter,instruction_register,settings)
			if settings['end_wait']:
				input('finished!')
			return 0
		#

		mstep = settings['micro_step'] and len(settings['memory_maps']) != 0 and is_memory_maps_accessed(memory,settings)
		step(mstep,'finished executing, ready to send data via memory mapped I/O...')

		#send data in memory maps
		enforce_memory_maps(memory,settings)

		step(mstep,'ready to fetch...')
		step(not mstep and settings['micro_step'],'finished executing, ready to fetch...')

		step(settings['step'] and not settings['micro_step'],'step...')

def is_memory_maps_accessed(memory,settings):
	maps = settings['memory_maps']
	for item in maps:
		if memory['fresh'].get(item[0]) == True:
			return True
	return False

def enforce_memory_maps(memory,settings):
	maps = settings['memory_maps']
	for item in maps:
		is_fresh = memory['fresh'].get(item[0])
		if is_fresh == True:
			data = sml.get_data(memory,item[0])
			sml.set_data(memory,item[0],item[1](data),settings)
			memory['fresh'][item[0]] = False

def parse_commands(prompt):
	while True:
		if not parse_command(input(prompt)):
			break

def parse_command(command_str):
	cs = command_str.split(' ')
	if cs[0] == 'doc' and len(cs) == 2:
		try:
			c = int(cs[1],16)
			show_name(c)
			show_doc(c)
		except:
			print('invalid instruction')
		return True
	elif len(command_str) == 0:
		return False
	else:
		return True

def show_name(instruction):
	print('operation name     : ', sml.operation_map[instruction].__name__)

def show_doc(instruction):
	print('operation documentation:')
	print('------------------------')
	print(sml.operation_map[instruction].__doc__)

def show_state(memory,registers,program_counter,instruction_register,settings):
	print('program_counter: ' + phex(program_counter,settings['reg_size']//4))
	print('instruction_register: ' + phex(instruction_register,settings['ins_reg_size']//4))
	print('memory:')
	print_data(memory,program_counter,p=settings['mu_size']//4)
	print('registers:')
	print_data(registers,None,p=settings['reg_size']//4)

def read_instruction(instruction_register,settings):
	bytes = sml.break_bytes(instruction_register,settings['ins_reg_size']//4)
	return (bytes[0],bytes[1:])

def load_data(data_file):
	data={}
	anno={}
	for line in data_file:
		if len(line) == 1 or line[0] == '#':
			continue
		l = line.split(" ")
		if len(l) == 2:
			address, info = l
		else:
			address = l[0]
			info = l[1]
			anno[int(address,16)] = str.join(' ',l[2:])[:-1]

		data[int(address,16)] = int(info,16)
	data['annotations'] = anno
	return data

def phex(s,p):
	r = hex(s)
	if len(r) < 2 + p or p == 0:
		pn = (2 + p - len(r))
		if pn < 0:
			pn = 0
		return '0x' + ('0' * pn) + r[2:]
	else:
		return r

def check_key(key):
	return type(key) == int

def _data_list(data,p):
	valid_data = False
	for key in data.keys():
		if check_key(key):
			valid_data = True
			break
	if valid_data:
		fp = max([ len(hex(key))-2 for key in data.keys() if check_key(key)])
	else:
		fp = 0
	return list(map(lambda x: (phex(x,fp),phex(data[x],p),data['annotations'][x]\
			if data['annotations'].get(x) != None else ''),\
			sorted([key for key in data.keys() if check_key(key)])))

def print_data(data,program_counter, head='\t', spacing=' : ', tail='\n', p=None):
	dl = _data_list(data,p=p)
	old_address = None
	if len(dl) > 0:
		old_address = int(dl[0][0],16) - 1
	for item in dl:
		new_address = int(item[0],16)
		if new_address != old_address + 1:
			print()
		if program_counter == new_address:
			s = '>>>>>'
		else:
			s = ''
		print(s + head + item[0] + spacing + item[1],item[2], end=tail)
		old_address = new_address

