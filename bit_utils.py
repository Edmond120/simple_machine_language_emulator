def overflow(integer, bits): #incomplete
	"""returns <integer>, truncating it if it exceeds <bits> bits"""
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
