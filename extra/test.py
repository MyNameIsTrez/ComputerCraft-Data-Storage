import numpy as np
import math
import time

def npLinalgNorm(b):
	begin1 = time.time()
	dist = np.linalg.norm(a - b)
	end1 = time.time()
	return end1 - begin1

def euclidean(b):
	begin2 = time.time()
	# Faster, but only works when count is equal to 3.
	# dist = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2
	dist = 0
	for i in range(count):
		dist += (a[i] - b[i]) ** 2
	end2 = time.time()
	return end2 - begin2

# <15 -> euclidean superior, >15 -> npLinalgNorm superior.
count = 30
print("count: {}".format(count))

a = np.random.randint(0, 256, size=count)

dt1 = 0
dt2 = 0

for _ in range(100000):
	dt1 += npLinalgNorm(np.random.randint(0, 256, size=count))
print("np.linalg.norm: {:.2f}s".format(dt1))

for _ in range(100000):
	dt2 += euclidean(np.random.randint(0, 256, size=count))
print("euclidean: {:.2f}s".format(dt2))

print("speed diff: {:.2%} / {:.2%}".format(dt1 / dt2, dt2 / dt1))