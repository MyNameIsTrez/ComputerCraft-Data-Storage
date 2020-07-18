def output(f, str):
	f.seek(0)
	f.truncate()
	f.write(str)
	f.flush()