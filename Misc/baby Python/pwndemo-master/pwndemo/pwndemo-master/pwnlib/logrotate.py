import traceback
from base64 import b64encode, b64decode

import MySQLdb

from pwnlib.logdata import logdata
from .log import getLogger

'''
A class for log rotate. this class will get data from sql database and print data or pack as a josn
'''


class logrotate(object):
    _sql = 'SELECT * FROM connections '
    _sql_id = 'con_id = %d '
    _sql_hash = 'con_hash = "%s" '
    _sql_token = 'token = "%s" '
    _sql_host = 'host = "%s" '
    _sql_ip = 'ip = "%s" '
    _sql_dport = 'dport = %d '
    _sql_sport = 'sport = %d'
    _sql_con_time = 'con_time > %d '
    _sql_fin_time = 'fin_time < %d '
    _sql_target = 'target = "%s" '

    _sql_flow = 'SELECT * FROM flow WHERE con_hash = "%s" '

    def __init__(self, sqluser, sqlpwd, host='localhost', database='pwnlog'):
        """
        The user name and password to the mysql database. the default database if pwnlog@localhost.
        """
        self._db = MySQLdb.connect(host, sqluser, sqlpwd, database)

    def find(self, **kwargs):
        """
        Find data.The key of kwargs is also the field of connections.
        use con_time and fin_time select the log between the times
        It's return a list of logdata class.Every logdata class is a pack of one pwn attach
        """

        tstr = self.make_sql(**kwargs)
        all_data = None
        try:
            csr = self._db.cursor()
            csr.execute(tstr)
            # print tstr
            all_data = csr.fetchall()
            csr.close()
        except:
            traceback.print_exc()
            self._db.rollback()

        return self.pack(all_data)

    def make_sql(self, **kwargs):
        """
        get the enter limited and return a sql cmd.
        """

        dataList = []
        dataList.append((self._sql_id, kwargs.get('con_id', None)))
        dataList.append((self._sql_hash, kwargs.get('con_hash', None)))
        token = kwargs.get('token', None)
        if token != None:
            token = b64encode(token)
        dataList.append((self._sql_token, token))
        dataList.append((self._sql_host, kwargs.get('host', None)))
        dataList.append((self._sql_ip, kwargs.get('ip', None)))
        dataList.append((self._sql_dport, kwargs.get('dport', None)))
        dataList.append((self._sql_sport, kwargs.get('sport', None)))
        dataList.append((self._sql_con_time, kwargs.get('con_time', None)))
        dataList.append((self._sql_fin_time, kwargs.get('fin_time', None)))
        dataList.append((self._sql_target, kwargs.get('target', None)))

        # make sql just add string together
        flag = False
        tstr = self._sql
        for data in dataList:
            if data[1] != None:
                if flag == False:
                    tstr += 'WHERE '
                    flag = True
                else:
                    tstr += 'AND '
                tstr += data[0] % data[1]

        return tstr

    def pack(self, allData):
        '''
        split the data to a list.and change the sql select data to a dict
        '''
        dataList = []
        for row in allData:
            IO_data = self.get_IO_data(row[1])  # use con_hash to find send and recv data in flow
            temp_dict = {}
            # temp_dict['con_id'] = row[0]
            # temp_dict['con_hash'] = row[1]
            temp_dict['token'] = b64decode(row[2])
            temp_dict['host'] = row[3]
            temp_dict['ip'] = row[4]
            temp_dict['dport'] = row[5]
            temp_dict['sport'] = row[6]
            temp_dict['con_time'] = row[7]
            temp_dict['fin_time'] = row[8]
            temp_dict['target'] = row[9]
            temp_dict['data'] = IO_data
            dataList.append(logdata(temp_dict))
        return dataList

    def get_IO_data(self, hash):
        """
        It's will use the hash two find the send and recv dates in flow table.And the data will sort by time.
        """
        temp_data = ()
        data = []
        try:
            csr = self._db.cursor()
            csr.execute(self._sql_flow % hash)
            temp_data = csr.fetchall()
            csr.close()
        except:
            traceback.print_exc()
            self._db.rollback()

        for row in temp_data:
            data.append((row[2], row[3], b64decode(row[4])))

        data.sort()

        return data
