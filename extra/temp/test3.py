import time
import numpy as np

list1 = [i for i in range(1000000)]
list2 = [i for i in range(1000000)]

start = time.time()

dot = 0

for i, j in zip(list1, list2):
	dot += i * j

end = time.time()

print(end - start)