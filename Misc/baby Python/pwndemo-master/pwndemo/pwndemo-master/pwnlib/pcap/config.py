def getToken():
    fp = open('/tmp/config','r')
    line = fp.readlines()
    fp.close()
    if len(line) < 1:
        return []
    else:
        return line[0][:-1].split(',')
def getKeyWord():
    fp = open('/tmp/config', 'r')
    line = fp.readlines()
    fp.close()
    if len(line) < 2:
        return []
    else:
        return line[1][:-1].split(',')