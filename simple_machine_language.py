def load_register_from_memory(memory,registers,settings,operand_bytes):
	"""Opcode 1, Operand RXY
	LOAD the register R with the bit pattern found in the memory cell whose
	address is XY.
	Example: 14A3 would cause the contents of the memory cell located at
	address A3 to be placed in register 4.
	"""
	R, XY = (operand_bytes[0],merge_bytes(*operand_bytes[1:]))

	registers[R] = memory[XY]


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

code_operation_map = {
	0x1 : load_register_from_memory,
}
