def getFlag():
	f  = open('./flag')
	flag = f.read()
	f.close()
	return flag
def message():
	spell = "Darkness beyond twilight Crimson beyond blood that flows Buried in the flow of time In thy great name, I pledge myself to darkness Let all the fools who stand in our way be destroyed by the power you and I possess...DRAGON SLAVE!"
	f = open('/dev/urandom')
	ran = f.read(16)
	spell += ran.encode('hex')
	f.close()
	return spell