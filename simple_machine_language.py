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
		return (ERROR,'Operation MOVE expected 0RS but recieved ' + operand_str)
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
	n1 = get_data(registers,S)
	n2 = get_data(registers,T)
	set_data(registers,R,n1 + n2,settings)
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

@operation(0x7)
def bitwise_or(memory,registers,settings,operand_bytes):
	"""Opcode 7, Operand RST
	OR the bit patterns in registers S and T and place the result in register R.
	Example: 7CB4 would cause the result of ORing the contents of registers B and 4 to be placed in
	register C.
	"""
	R, S, T = operand_bytes[:]
	bp1 = get_data(registers,S)
	bp2 = get_data(registers,T)
	result = bp1 | bp2
	set_data(registers,R,result,settings)
	return (SUCCESS,)

@operation(0x8)
def bitwise_and(memory,registers,settings,operand_bytes):
	"""Opcode 8, Operand RST
	AND the bit patterns in register S and T and place the result in register R.
	Example: 8045 would cause the result of ANDing the contents of registers 4 and 5 to be placed in
	register 0.
	"""
	R, S, T = operand_bytes[:]
	bp1 = get_data(registers,S)
	bp2 = get_data(registers,T)
	result = bp1 & bp2
	set_data(registers,R,result,settings)
	return (SUCCESS,)

@operation(0x9)
def bitwise_exclusive_or(memory,registers,settings,operand_bytes):
	"""Opcode 9, Operand RST
	EXCLUSIVE OR the bit patterns in registers S and T and place the result in register R.
	Example: 95F3 would cause the result of EXCLUSIVE ORing the contents of registers F and 3 to
	be placed in register 5.
	"""
	R, S, T = operand_bytes[:]
	bp1 = get_data(registers,S)
	bp2 = get_data(registers,T)
	result = bp1 ^ bp2
	set_data(registers,R,result,settings)
	return (SUCCESS,)

@operation(0xA)
def bitwise_rotate(memory,registers,settings,operand_bytes):
	"""Opcode A, Operand R0X
	ROTATE the bit pattern in register R one bit to the right X times. Each time place the bit that
	started at the low-order end at the high-order end.
	Example: A403 would cause the contents of register 4 to be rotated 3 bits to the right in a circular
	fashion.
	"""
	if operand_bytes[1] != 0x0:
		operand_str = str.join(' ',map(hex,operand_bytes))
		return (ERROR,'Operation ROTATE expected R0X but recieved ' + operand_str)
	R, X = (operand_bytes[0],operand_bytes[2])

	value = get_data(registers,R)
	bits = settings['reg_size']

	value = bit_rotate_right(value,bits,X)

	set_data(registers,R,value,settings)
	return (SUCCESS,)

@operation(0xB)
def jump(memory,registers,settings,operand_bytes):
	"""Opcode B, Operand RXY
	JUMP to the instruction located in the memory cell at address XY if the bit pattern in register R
	is equal to the bit pattern in register number 0. Otherwise, continue with the normal sequence of
	execution. (The jump is implemented by copying XY into the program counter during the execute
	phase.)
	Example: B43C would first compare the contents of register 4 with the contents of register 0. If
	the two were equal, the pattern 3C would be placed in the program counter so that the next
	instruction executed would be the one located at that memory address. Otherwise, nothing would
	be done and program execution would continue in its normal sequence.
	"""
	R, XY = (operand_bytes[0],merge_bytes(*operand_bytes[1:]))
	if get_data(registers,0) == get_data(registers,R):
		return (JUMP,XY)
	else:
		return (SUCCESS,)

@operation(0xC)
def halt_execution(memory,registers,settings,operand_bytes):
	"""Opcode C, Operand 000
	HALT execution.
	Example: C000 would cause program execution to stop.
	"""
	if operand_bytes != [0,0,0]:
		operand_str = str.join(' ',map(hex,operand_bytes))
		return (ERROR,'Operation HALT expected 000 but recieved ' + operand_str)
	return (END,)
#

def set_data(dic,key,value,settings):
	if dic['data_type'] == 'registers':
		dic[key] = overflow(value,settings['reg_size'])
	elif dic['data_type'] == 'memory':
		dic[key] = overflow(value,settings['mu_size'])
	else:
		raise ValueError('unexpected argument value')

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
