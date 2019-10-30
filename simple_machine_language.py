from functools import wraps

from bit_utils import *

#messages
SUCCESS = 0
ERROR = 1
END = 2
JUMP = 3

#keys are ints, values are functions
operation_map = {}

def operation(opcode):
	def decorator(func):
		operation_map[opcode] = func
		return func
	return decorator

#operation functions
#return value, should be a tuple where the first item is a message (int)
@operation(0x1)
def load_register_from_memory(memory,registers,settings,operand_bytes):
	"""Opcode 1, Operand RXY
	LOAD the register R with the bit pattern found in the memory cell whose
	address is XY.
	Example: 14A3 would cause the contents of the memory cell located at
	address A3 to be placed in register 4.
	"""
	R, XY = (operand_bytes[0],merge_bytes(*operand_bytes[1:]))

	set_data(registers,R,get_data(memory,XY),settings)
	return (SUCCESS,)

@operation(0x2)
def load_register_with_bit_pattern(memory,registers,settings,operand_bytes):
	"""Opcode 2, Operand RXY
	LOAD the register R with the bit pattern XY.
	Example: 20A3 would cause the value A3 to be placed in register 0.
	"""
	R, XY = (operand_bytes[0],merge_bytes(*operand_bytes[1:]))

	set_data(registers,R,XY,settings)
	return (SUCCESS,)

@operation(0x3)
def store(memory,registers,settings,operand_bytes):
	"""Opcode 3, Operand RXY
	STORE the bit pattern found in register R in the memory cell whose address
	is XY.
	Example: 35B1 would cause the contents of register 5 to be placed in the
	memory cell whose address is B1.
	"""
	R, XY = (operand_bytes[0],merge_bytes(*operand_bytes[1:]))

	set_data(memory,XY,get_data(registers,R),settings)
	return (SUCCESS,)

@operation(0x4)
def move(memory,registers,settings,operand_bytes):
	"""Opcode 4, Operand 0RS
	MOVE the bit pattern found in register R to register S.
	Example: 40A4 would cause the contents of register A to be copied into register 4.
	"""
	if operand_bytes[0] != 0x0:
		operand_str = str.join(' ',map(hex,operand_bytes))
		raise ValueError('Operation MOVE expected 0RS but recieved ' + operand_str)
	R, S = (operand_bytes[1],operand_bytes[2])

	set_data(registers,S,get_data(registers,R),settings)
	return (SUCCESS,)

@operation(0x5)
def twos_complement_add(memory,registers,settings,operand_bytes):
	"""Opcode 5, Operand RST
	ADD the bit patterns in registers S and T as though they were two’s
	complement representations and leave the result in register R.
	Example: 5726 would cause the binary values in registers 2 and 6 to be
	added and the sum placed in register 7.
	"""
	R, S, T = operand_bytes[:]

	n1, n2 = (us_to_tc(get_data(registers,S),settings['mu_size']),
			  us_to_tc(get_data(registers,T),settings['mu_size']))
	set_data(registers,R,tc_to_us(n1 + n2),settings)
	return (SUCCESS,)

@operation(0x6)
def floating_point_add(memory,registers,settings,operand_bytes): #incomplete
	"""Opcode 6, Operand RST
	ADD the bit patterns in registers S and T as though they represented values in floating-point
	notation and leave the floating-point result in register R.
	Example: 634E would cause the values in registers 4 and E to be added as floating-point values
	and the result to be placed in register 3.
	"""
	R, S, T = operand_bytes[:]

	return (ERROR,"incomplete function")
#

def set_data(dic,key,value,settings):
	dic[key] = overflow(value,settings['mu_size'])

def get_data(dic,key):
	item = dic.get(key)
	if item == None:
		return 0
	else:
		return item

def break_bytes(operand,operand_size):
	bytes = [0] * operand_size
	for i in range(operand_size - 1,-1,-1):
		bytes[i] = operand % 16
		operand = int(operand / 16)
	return bytes

def merge_bytes(*bytes):
	operand = 0
	for i in range(len(bytes)):
		operand *= 16
		operand += bytes[i]
	return operand
