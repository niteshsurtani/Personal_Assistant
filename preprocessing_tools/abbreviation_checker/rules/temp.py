abr = []
f = open("w","r")
for line in f:
	abr.append(line.strip())
	
f1 = open("location","r")
for line in f1:
	lc = line.split()
	loc = lc[0].strip()
	if loc not in abr:
		print line,


