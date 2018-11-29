import dpkt

from pwnlib import sqllog
from pwnlib.daemons import listened
from pwnlib.pcap.config import getToken
from pwnlib.pcap.pcapDecode import addQueue, start, finishDecode
from pwnlib.timeout import Timeout

#token_list = ['misaka']


class pcapLister():
    def __init__(self, port=0, bindaddr="0.0.0.0",
                 fam="any", typ="tcp",
                 timeout=90):
        self.port = port
        self.bindaddr = bindaddr
        self.fam = fam
        self.typ = typ
        self.Timeout = timeout
        start()

    def set_sql(self, sqluser, sqlpwd, host='localhost', database='pwnlog'):
        sqllog.set_sql(sqluser, sqlpwd, host, database)
        sqllog.sql_on = True

    def __call__(self):
        with listened(self.port, self.bindaddr, self.fam, self.typ, self.Timeout) as listen:
            if listen == None:
                finishDecode()
                return

            listen.close_info_log(True)
            token = listen.recvline()[:-1]
            if token in getToken():
                info = tuple(listen.recvline()[:-1].split(','))
                if len(info) != 2:
                    listen.close()
                    return

                data = listen.recvline()[:-1]
                addQueue(data, info)
            listen.close()
