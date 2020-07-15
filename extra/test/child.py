import os

foo = bytearray('{"dt" : "This is a test"}\n', 'utf8')
print(foo)
os.write(3, foo)