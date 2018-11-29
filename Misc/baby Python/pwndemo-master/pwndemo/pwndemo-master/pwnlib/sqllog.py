import base64
from hashlib import md5

import MySQLdb
import traceback
import time
import log

"""
It use mysql to stone all pwn attack logs.Just use logrotate to review logs.
"""
logger = log.getLogger('pwnlib.sqllog')
recv = 1
send = 0


class sqllog(object):
    _consqlstr = 'INSERT INTO connections(con_hash,token,host,ip,dport,sport,con_time,fin_time,target) ' \
                 'VALUES("%s","%s","%s","%s",%d,%d,%f,%f,"%s");'

    _dsqlstr = 'INSERT INTO flow(con_hash,time,flag,data) VALUES("%s",%f,%d,"%s");'

    _find_table = 'SELECT table_name FROM information_schema.TABLES WHERE table_name ="%s";'

    _creat_connections = 'create table if not exists connections( ' \
                         'con_id INT(11) NOT NULL AUTO_INCREMENT ,' \
                         'con_hash CHAR(45) NOT NULL , ' \
                         'token VARCHAR(100) DEFAULT NULL ,' \
                         'host CHAR(16) NOT NULL , ' \
                         'ip char(16) NOT NULL, ' \
                         'dport INT(11) NOT NULL , ' \
                         'sport INT(11) NOT NULL, ' \
                         'con_time DOUBLE NOT NULL , ' \
                         'fin_time DOUBLE NOT NULL , ' \
                         'target VARCHAR(1024) DEFAULT NULL ,' \
                         'PRIMARY KEY (con_id)' \
                         ');'

    _flow = 'create table if not exists flow(' \
            'id INT(11) NOT NULL AUTO_INCREMENT,' \
            'con_hash CHAR(45) NOT NULL , ' \
            'time DOUBLE NOT NULL , ' \
            'flag INT(11) NOT NULL , ' \
            'data MEDIUMTEXT, ' \
            'PRIMARY KEY (id)' \
            ');'

    recv = 1
    send = 0

    def __init__(self, sqluser, sqlpwd, host='localhost', database='pwnlog'):
        """
        The argument for connect mysql.This class will hold the handle of the connect.
        It will check if there is connection and flow table in the database.It will auto create tables
        """
        self._db = MySQLdb.connect(host, sqluser, sqlpwd, database)
        csr = self._db.cursor()

        # The table check
        tstr = self._find_table % ('connections',)
        csr.execute(tstr)

        if len(csr.fetchall()) == 0:
            self.creat_table('connections')

        tstr = self._find_table % ('flow',)
        csr.execute(tstr)
        if len(csr.fetchall()) == 0:
            self.creat_table('flow')
        csr.close()
        self.is_init = False

    def log_new_connection(self, client, target, t=None):
        """
        Init when get a new connect.
        The client is a tuple with three element like this -> (host,port,token)
        take the ip port and token and init the class.The log will insert into database after the connect end
        The argument t is the time.use current time stamp as default
        """
        if t == None:
            t = time.time()
        self._con_time = t
        self._host, self._dport, self._token = client
        self._token = base64.b64encode(self._token)
        self._con_hash = md5('%s:%d-%f' % (self._host, self._dport, self._con_time)).hexdigest()
        self._target, self._ip, self._sport = target
        self.is_init = True

    def log_data(self, data, flag, t=None):
        """
        inset the send or recv data to database.
        Use flag show be sqllog.recv or sqllog.send to show the data is recv data or send data
        The argument t is the time.use current time stamp as default
        """
        if t == None:
            t = time.time()
        if self.is_init == False:
            logger.error('Please call log_new_connection method before')

        tstr = self._dsqlstr % (self._con_hash, t, flag, base64.b64encode(data))
        try:
            csr = self._db.cursor()
            csr.execute(tstr)
            self._db.commit()
            csr.close()
        except:
            traceback.print_exc()
            self._db.rollback()

    def log_finish(self, t=None):
        """
        get the finish time of the connect.and log connect data to database
        The argument t is the time.use current time stamp as default
        """
        if t == None:
            t = time.time()
        tstr = self._consqlstr % (self._con_hash,
                                  self._token,
                                  self._host,
                                  self._ip,
                                  self._dport,
                                  self._sport,
                                  self._con_time,
                                  t,
                                  self._target)

        try:
            csr = self._db.cursor()
            csr.execute(tstr)
            self._db.commit()
            csr.close()
            self.close()
        except:
            traceback.print_exc()
            self._db.rollback()

    def creat_table(self, table='connections'):
        """
        the method to create table user sql cmd
        """
        if table == 'connections':
            tstr = self._creat_connections
        elif table == 'flow':
            tstr = self._flow
        else:
            return
        try:
            csr = self._db.cursor()
            csr.execute(tstr)
            self._db.commit()
            csr.close()
        except:
            traceback.print_exc()
            self._db.rollback()

    def close(self):
        """
        close database connection
        """
        self._db.close()

    def update_handle(self, sqluser, sqlpwd, host='localhost', database='pwnlog'):
        """
        use to get a new connection hand.user when fork a new process
        """
        self._db = MySQLdb.connect(host, sqluser, sqlpwd, database)

    def logFromPack(self, data):
        temp_dict = data.get_dict()
        self.log_new_connection((temp_dict['host'], temp_dict['dport'], temp_dict['token']),
                                (temp_dict['target'], temp_dict['ip'], temp_dict['sport']),
                                temp_dict['con_time'])
        for data in temp_dict['data']:
            self.log_data(data[2], data[1], data[0])
        self.log_finish(temp_dict['fin_time'])


sql = None
sql_on = False
sql_info = {}


def set_sql(sqluser, sqlpwd, host='localhost', database='pwnlog'):
    """
    The func to get sqllog class.and stone the connection user info
    """
    global sql
    global sql_on
    global sql_info
    sql_info['sqluser'] = sqluser
    sql_info['sqlpwd'] = sqlpwd
    sql_info['host'] = host
    sql_info['database'] = database

    sql = sqllog(sqluser, sqlpwd, host, database)
    sql_on = True
    return sql


def updata_sql():
    """
    get a new sqlclass with the stone user info
    """
    global sql
    global sql_info
    sql.update_handle(sql_info['sqluser'], sql_info['sqlpwd'], sql_info['host'], sql_info['database'])
    return sql
