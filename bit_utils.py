def overflow(integer, bits):
	"""returns <integer>, truncating it if it exceeds <bits> bits"""
	max = 2 ** bits - 1
	if integer <= max:
		return integer

	most_sig_bit_value = 1
	while integer >= most_sig_bit_value * 2:
		most_sig_bit_value *= 2
	while integer > max:
		integer -= most_sig_bit_value
		most_sig_bit_value //= 2
	return integer

def us_to_tc(unsigned_int, bits):
	"""
	returns the number unsigned_int would be if it was in two's complement
	notation
	"""
	if (2 ** (bits - 1)) <= unsigned_int:
		#negative
		return unsigned_int - 2**bits
	else:
		#positive
		return unsigned_int

def tc_to_us(twos_complement_int, bits):
	"""
	returns the number twos_complement_int would be if it was treated as an
	unsigned int notation
	"""
	if twos_complement_int >= 0:
		return twos_complement_int
	else:
		return twos_complement_int + 2**bits

def bit_rotate_right(value,bits,times):
	most_sig_bit_value = 2 ** (bits - 1)
	for i in range(times):
		right_most_bit = value % 2
		value //= 2 #shift
		if right_most_bit != 0:
			value += most_sig_bit_value
	return value
