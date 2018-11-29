from pwn import *
import gmpy2
#p = process('./do.sh')
p=remote('ctfgame.acdxvfsvd.net', 30002)
p.recvuntil('Token')
p.sendline('qOpWXS71aNF5TfefMG50WgBFtcSOaxPU')
p.recvuntil('something:\n')
c = gmpy2.mpfr(p.recvline()[:-1])
s = ''
while True:
	re = p.recvuntil('l1',timeout=2)
	if not re:
		break
	p.recvuntil(']:\n')
	l1 = p.recvline()[:-1]
	l1 = gmpy2.mpfr(l1)
	p.recvuntil('l2')
	p.recvuntil(']:\n')
	l2 = p.recvline()[:-1]
	l2 = gmpy2.mpfr(l2)
	a = (l1+l2)/2.0
	e = c/a
	ch = int(round((((l1-a)/e)/a)*128.0))
	s+=chr(ch)

print s 
p.recvuntil('Now tell me what homura said?')
p.sendline(s)
p.interactive()