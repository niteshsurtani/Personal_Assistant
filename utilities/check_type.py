def isNumber(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def isDateToken(token):
	date_extensions = ['st','nd','rd','th']

	last_two = token[-2:]
	till_last_two = token[:-2]

	if last_two in date_extensions and isNumber(till_last_two):
		val = int(till_last_two)
		if val <= 31:
			return val
		else:
			return 0
	return 0