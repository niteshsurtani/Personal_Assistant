from time import time

for i in range(0,3):
	time1 = time()
	
	for j in range(0,10000000):
		continue

	time1 = time() - time1
	print time1