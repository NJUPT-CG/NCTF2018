#! /usr/bin/python
import os
import socket
import subprocess

import fcntl

import select
import threading
from base64 import b64encode

import signal

from multiprocessing import Queue


class tcpdunmp():
    cmd = ['tcpdump', '-i', 'lo', 'port', '9999', '-n', '-B', '1080', '-s', '0', '-w', '-']
    IP = '127.0.0.1'
    PORT = 12345
    NAME = 'misaka'
    token = 'a token'
    target = 'a target'

    def __init__(self):
        self.queue = Queue()
        PIPE = subprocess.PIPE
        self.p = subprocess.Popen(self.cmd, stdout=PIPE)

        flags = fcntl.fcntl(self.p.stdout.fileno(), fcntl.F_GETFL)
        fcntl.fcntl(self.p.stdout.fileno(), fcntl.F_SETFL, (flags | os.O_NDELAY | os.O_NONBLOCK))
        self.out = self.p.stdout
        threading.Thread(target=self.sendData).start()

    def __call__(self):
        try:
            while True:
                if select.select([self.out.fileno()], [], [], 0.1) == ([self.out.fileno()], [], []):
                    data = ''
                    try:
                        while True:
                            data += self.out.read(4096)
                    except IOError:
                        tmp = ''.join(data)
                        len(tmp)
                        self.queue.put(tmp)
                        tmp = ''
                    finally:
                        data = ''

        except KeyboardInterrupt:
            os.kill(self.pid, signal.SIGTERM)

    def sendData(self):
        self.pid = os.getpid()
        while True:
            data1 = self.queue.get()
            tmp = ''.join(data1)
            data = b64encode(tmp)
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.connect((self.IP, self.PORT))
            self.sendLine(s, self.NAME)
            self.sendLine(s, self.token + ',' + self.target)
            self.sendLine(s, data)
            s.close()

    def sendLine(self, s, data):
        try:
            s.sendall(data + '\n')
        except:
            exit(0)


if __name__ == '__main__':
    p = tcpdunmp()
    p()
