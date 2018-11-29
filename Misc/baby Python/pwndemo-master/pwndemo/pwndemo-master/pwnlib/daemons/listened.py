import time

import signal

from ..tubes.listen import listen
from ..timeout import Timeout
import os
from .. import log
import threading

logger = log.getLogger('pwnlib.listened')


class wait_child(threading.Thread):
    def __init__(self):
        super(wait_child, self).__init__()
        self.pid = 0

    def run(self):
        self.pid = os.getpid()
        while True:
            try:
                os.wait()
            except OSError:
                time.sleep(0.5)
                continue
                # def end(self):
                # pass


class listened():
    def __init__(self, port=0, bindaddr="0.0.0.0",
                 fam="any", typ="tcp",
                 timeout=Timeout.default):
        self.port = port
        self.bindaddr = bindaddr
        self.fam = fam
        self.typ = typ
        self.timeout = timeout

        self.listen_handle = listen(port, bindaddr, fam, typ, timeout)
        self.w = wait_child()
        self.w.start()
        # signal.signal(signal.SIGTERM,self.w.end)

    def __enter__(self):
        try:
            while True:
                self.listen_handle.wait_for_connection()
                self.pid = os.fork()
                if self.pid == 0:
                    return self.listen_handle
                else:
                    # time.sleep(0.3)
                    self.listen_handle = listen(self.port, self.bindaddr, self.fam, self.typ, self.timeout)
        except KeyboardInterrupt:
            self.listen_handle.close()
            if self.w.pid != 0:
                os.kill(self.w.pid, signal.SIGTERM)
            return None

    def __exit__(self, exc_type, exc_val, exc_tb):
        # self.listen_handle.close()
        # exit(0)
        pass
