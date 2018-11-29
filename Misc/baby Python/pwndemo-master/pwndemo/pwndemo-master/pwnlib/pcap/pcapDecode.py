import os
import threading

import StringIO
import dpkt
import time
import signal
import socket

from base64 import b64decode

from multiprocessing import Queue

from pwnlib import sqllog
from pwnlib.logdata import logdata


class pcapDecode(threading.Thread):
    #fileName = '/tmp/pcapTempData'

    def __init__(self):
        super(pcapDecode, self).__init__()
        self.i = 0
        self.pid = 0
        self.linkList = []
        self.io = StringIO.StringIO()
        self.fileHead = ''

    def run(self):
        self.pid = os.getpid()
        while True:
            data, info = pcapQueue.get()
            self.decodeData(data, info)

    def findDict(self, src, dst, sport, dport):
        i = 0
        Len = len(self.linkList)
        while i < Len:
            temp_dict = self.linkList[i]
            if temp_dict['host'] == dst and \
                    temp_dict['ip'] == src and \
                    temp_dict['dport'] == dport and \
                    temp_dict['sport'] == sport:
                return i
            i += 1
        return None

    def decodeData(self, data, info):
        data = b64decode(data)
        if self.fileHead == '':
            self.fileHead = data[:24]
        self.io.write(data)
        self.io.seek(0)

        pcapReader = dpkt.pcap.Reader(self.io)

        pos = self.io.pos
        Pos2 = pos
        ether2 = None
        ts2 = 0
        try:
            ts2, data = pcapReader.next()
            ether2 = dpkt.ethernet.Ethernet(data)
            Pos2 = self.io.pos
        except dpkt.NeedData:
            print  'need data'
            self.io.seek(pos)
            tmp = self.io.read()
            self.io.close()
            self.io = StringIO.StringIO()
            self.io.write(self.fileHead + tmp)
            return
        except StopIteration:
            print 'inter'
            self.io.seek(pos)
            tmp = self.io.read()
            self.io.close()
            self.io = StringIO.StringIO()
            self.io.write(self.fileHead + tmp)
            return

        while True:
            ether = ether2
            ts = ts2
            try:
                ts2, data = pcapReader.next()
                ether2 = dpkt.ethernet.Ethernet(data)
                pos = Pos2
                Pos2 = self.io.pos
            except dpkt.NeedData:
                self.io.seek(pos)
                tmp = self.io.read()
                self.io.close()
                self.io = StringIO.StringIO()
                self.io.write(self.fileHead + tmp)
                break
            except StopIteration:
                self.io.seek(pos)
                tmp = self.io.read()
                self.io.close()
                self.io = StringIO.StringIO()
                self.io.write(self.fileHead + tmp)
                break
                # for ts, data in pcapReader:
                #     try:
                #         ether = dpkt.ethernet.Ethernet(data)
                #         pos = self.io.pos
                #     except dpkt.NeedData:
                #         self.io.seek(pos)
                #         tmp = self.io.read()
                #         self.io.seek(24)
                #         self.io.write(tmp)

            if ether.type == dpkt.ethernet.ETH_TYPE_IP:
                ip = ether.data

                try:
                    src = socket.inet_ntoa(ip.src)
                    dst = socket.inet_ntoa(ip.dst)
                except AttributeError:
                    fp = open('/tmp/tttt', 'a')
                    fp.write(ip + '\n')
                    fp.close()
                    continue

                getData = ip.data

                if isinstance(getData, dpkt.tcp.TCP):
                    dport = getData.dport
                    sport = getData.sport
                    if getData.flags & dpkt.tcp.TH_SYN \
                        and getData.flags & dpkt.tcp.TH_ACK:
                        temp_dict = {}
                        temp_dict['token'] = info[0]
                        temp_dict['target'] = info[1]
                        temp_dict['host'] = dst
                        temp_dict['ip'] = src
                        temp_dict['dport'] = dport
                        temp_dict['sport'] = sport
                        temp_dict['con_time'] = ts
                        temp_dict['data'] = []
                        # print temp_dict
                        self.linkList.append(temp_dict)

                    elif getData.flags & dpkt.tcp.TH_FIN:
                        id = self.findDict(src, dst, sport, dport)
                        if id == None:
                            continue
                        temp_dict = self.linkList[id]
                        temp_dict['fin_time'] = ts
                        temp_dict['data'].sort()
                        packData = logdata(temp_dict)
                        self.linkList.pop(id)
                        if packData.level() >= 0:
                            packData.show()
                            self.i += 1
                            # print '--------------------------------------------------------------------'
                            # print self.i
                        # print "show over"
                        if sqllog.sql_on == True:
                            sqllog.updata_sql()
                            sqllog.sql.logFromPack(packData)

                    elif getData.flags & dpkt.tcp.TH_PUSH:
                        # print getData.data
                        flag = sqllog.send
                        id = self.findDict(src, dst, sport, dport)
                        if id == None:
                            id = self.findDict(dst, src, dport, sport)
                            flag = sqllog.recv
                            if id == None:
                                continue

                        temp_dict = self.linkList[id]
                        temp_dict['data'].append((ts, flag, getData.data))


def addQueue(data, info):
    pcapQueue.put((data, info))


def finishDecode():
    if pcap.pid != 0:
        os.kill(pcap.pid, signal.SIGTERM)


pcap = None
pcapQueue = None


def start():
    global pcap, pcapQueue
    pcapQueue = Queue()
    pcap = pcapDecode()
    pcap.start()
