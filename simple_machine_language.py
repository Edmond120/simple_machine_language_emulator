from bit_utils import *

def load_register_from_memory(memory,registers,settings,operand_bytes):
	"""Opcode 1, Operand RXY
	LOAD the register R with the bit pattern found in the memory cell whose
	address is XY.
	Example: 14A3 would cause the contents of the memory cell located at
	address A3 to be placed in register 4.
	"""
	R, XY = (operand_bytes[0],merge_bytes(*operand_bytes[1:]))

	set_data(registers,R,memory[XY],settings)

def load_register_with_bit_pattern(memory,registers,settings,operand_bytes):
	"""Opcode 2, Operand RXY
	LOAD the register R with the bit pattern XY.
	Example: 20A3 would cause the value A3 to be placed in register 0.
	"""
	R, XY = (operand_bytes[0],merge_bytes(*operand_bytes[1:]))

	set_data(registers,R,XY,settings)

def store(memory,registers,settings,operand_bytes):
	"""Opcode 3, Operand RXY
	STORE the bit pattern found in register R in the memory cell whose address
	is XY.
	Example: 35B1 would cause the contents of register 5 to be placed in the
	memory cell whose address is B1.
	"""
	R, XY = (operand_bytes[0],merge_bytes(*operand_bytes[1:]))

	set_data(memory,XY,registers[R],settings)


def set_data(dic,key,value,settings):
	dic[key] = overflow(value,settings['memory_unit_bit_size'])

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

operation_map = {
	0x1 : load_register_from_memory,
	0x2 : load_register_with_bit_pattern,
	0x3 : store,
}
