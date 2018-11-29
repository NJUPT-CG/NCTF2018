import gmpy2
import random
import GetFlag
c = random.uniform(100000000,1000000000000)
c = gmpy2.mpfr(c)
print "Homura sent some message after disappearing."
print "But it was encoded and no one can understand it."
print "Fortunately you find something:"
print c
print "May be it will be useful."
flag = GetFlag.getFlag()
mess = GetFlag.message()
i = 1
print "Here is the encoded message"
for ch in mess:
	b = random.uniform(10000000000,1000000000000)
	b = gmpy2.mpfr(b)
	a = gmpy2.root(b*b+c*c,2)	
	x = gmpy2.mpfr((gmpy2.mpfr(ord(ch))/128.0)*(a))
	y = gmpy2.root((b*b-((b*b)/(a*a))*(x*x)),2)
	l1 = gmpy2.root((((x+c)**2)+(y**2)),2)
	l2 = gmpy2.root((((x-c)**2)+(y**2)),2)
	print "l1[%d]:"%i
	print l1
	print "l2[%d]:"%i
	print l2
	i+=1

print "Now tell me what homura said?"
ans = raw_input()
if ans == mess:
	print flag
else:
	print "No you did not understand what homura said."

