#! /usr/bin/python
import pwn
import hashlib

def getFlag(token):
	sha256 = hashlib.sha256()
	key = '_Y1g_666_7Q1_0o0!'
	key += token
	sha256.update(key)
	flag = 'NCTF{'+sha256.hexdigest()+'}'
	return flag


a = pwn.daemon(60)  # A demon class,The argument is the second of time out, 0 is no timeout

a.set_listen(2360)  # The port you want to listen
a.set_process('/home/ctf/bin/do.sh', cwd='/home/pwn')  # first argument is the binary,
# make sure other has permission of execute for it
#a.set_sql('explorer', '123456')  # The name and password of mysql. Default it will log data in database pwnlog.
# But you can easy change it.And dot't worry of table.I will create it
a.open_permission()
a(getFlag)  # start it
