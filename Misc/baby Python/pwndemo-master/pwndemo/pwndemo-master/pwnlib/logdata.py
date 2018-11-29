import json
import logging
import string
from time import ctime

from pwnlib import sqllog
from pwnlib.pcap.config import getKeyWord
from .log import getLogger
from pwnlib.util import fiddling

log = getLogger('pwnlib.rotate')


class logdata(object):
    """
    A class for stone log data.It's easy to get a json or a dict from it.Or just show it.
    """

    def __init__(self, data):
        """
        The class is made by logrotate and this function show not call by others
        """
        self._data = data
    def level(self):
        key = getKeyWord()
        level = 0
        datas = self._data['data']
        for data in datas:
            for word in key:
                if data[2].find(word) != -1:
                    level += 1
        return level


    def show(self):
        """
        show the log data after format
        """
        log.info('%s:%d get a connnection to %s at %s' % (self._data['ip'],
                                                          self._data['sport'],
                                                          self._data['target'],
                                                          ctime(self._data['con_time'])))

        log.info('The connection from %s:%d' % (self._data['host'], self._data['dport']))
        if self._data['token'] != '':
            log.info('Token is: %s' % self._data['token'])

        datas = self._data['data']

        for data in datas:
            if data[1] == sqllog.recv:
                log.recv('Received %#x bytes At %s: ' % (len(data[2]), ctime(data[0])))
            elif data[1] == sqllog.send:
                log.send('Sent %#x bytes At %s:' % (len(data[2]), ctime(data[0])))

            if len(set(data[2])) == 1:
                log.indented('%r * %#x' % (data[2][0], len(data[2])), level=logging.INFO)
            elif all(c in string.printable for c in data[2]):
                for line in data[2].splitlines(True):
                    log.indented(repr(line), level=logging.INFO)
            else:
                log.indented(fiddling.hexdump(data[2]), level=logging.INFO)

    def get_josn(self):
        """
        dumps a json of data
        """
        return json.dumps(self._data)

    def get_dict(self):
        """
        just return the dict it stone
        """
        return self._data

