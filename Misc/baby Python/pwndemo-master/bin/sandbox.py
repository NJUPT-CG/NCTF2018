#!/usr/bin/python

from __future__ import print_function

print("Welcome to yulige's Python sandbox! Enter commands below!")
print("Could you bypass it?")
Th1s_1S_WAF = [  
    "import",
    "exec",
    "eval",
    "pickle",
    "os",
    "subprocess",
    "input",
    "cry sum more",
    "sys",
    "linecache",
    "globals",
    "flag",
    "file",
    "pop",
    "getattr",
    "class",
    "mro",
    "bases",
    "subclasses",
   "init",
    "]","["]

targets = __builtins__.__dict__.keys()  
targets.remove('raw_input')  
targets.remove('print')
targets.remove('dir')
for x in targets:
    del __builtins__.__dict__[x]
while 1:  
    print(">>>", end=' ')
    data = raw_input()
    for no in Th1s_1S_WAF:
        if no.lower() in data.lower():
            print("No!Y0u 4r3 A baby H4ck3r...")
            break
    else:
        try: 
           exec data
        except:
           print("Wh4t_Th3_Err0r?")
