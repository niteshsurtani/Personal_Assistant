def typec(val,from1,to):
	if (from1 == 'string'): 
		if (to == 'integer'):
			try:
				val = int(val)
				return val
			except:
				return None

	if (from1 == 'string'): 
		if (to == 'string'):
			try:
				val = str(val)
				return val
			except:
				return None
	if (from1 == 'string'): 
		if (to == 'float'):
			try:
				val = float(val)
				return val
			except:
				return None