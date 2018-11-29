import os
import time

import subprocess
from pwd import getpwnam
from random import randint, seed
from .. import context
from ..timeout import Timeout
from .listened import listened
from .. import tubes
from ..tubes.process import PIPE, PTY, STDOUT
from .. import timeout
from .. import log
from .. import sqllog

logger = log.getLogger('pwnlib.daemon')


class daemon(Timeout):
    def __init__(self, timeout=90):
        if timeout == 0:
            timeout = Timeout.forever
        self.permission = False
        super(daemon, self).__init__(timeout)

    def set_listen(self, port=0, bindaddr="0.0.0.0",
                   fam="any", typ="tcp",
                   timeout=Timeout.default):
        self.port = port
        self.bindaddr = bindaddr
        self.fam = fam
        self.typ = typ
        self.Timeout = timeout

    def set_process(self, argv,
                    shell=False,
                    executable=None,
                    cwd=None,
                    env=None,
                    timeout=Timeout.default,
                    stdin=PIPE,
                    stdout=PTY,
                    stderr=STDOUT,
                    close_fds=True,
                    preexec_fn=lambda: None):
        cwd = cwd or os.path.curdir
        if cwd != '/':
            cwd += '/'
        self.argv = argv
        self.shell = shell
        self.executable = executable
        self.cwd = cwd
        self.env = env
        self.out = timeout
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr
        self.close_fds = close_fds
        self.preexec_fn = preexec_fn

    def __call__(self, getFlag=None):
        with listened(self.port, self.bindaddr, self.fam, self.typ, self.Timeout) as listen:
            if listen == None:
                return
            listen.sendline('Your Token:')
            self.token = listen.recvuntil('\n')[:-1]
            if len(self.token)!=32:
                listen.sendline('Wrong token')
                listen.close()
                return
            if sqllog.sql_on == True:
                self.sql_init(listen)
            if self.permission:
                self._set_env(getFlag)
            pid = os.fork()
            if pid == 0:
                try:
                    if sqllog.sql_on == True:
                        sqllog.updata_sql()
                    if self.permission:
                        self._set_permission()
                    process = tubes.process.process(self.argv,
                                                    self.shell,
                                                    self.executable,
                                                    self.cwd,
                                                    self.env,
                                                    self.out,
                                                    self.stdin,
                                                    self.stdout,
                                                    self.stderr,
                                                    self.close_fds,
                                                    self.preexec_fn)
                    process.close_info_log(True)
                    process.connect_both(listen)
                    with self.countdown():
                        while self.countdown_active():  # shutdown process if time out
                            time.sleep(0.1)
                            if process.poll() != None:
                                break  # don't count if process if end
                        if not self.countdown_active():
                            listen.sendline('Sorry timeout')
                    process.close()
                    # listen.close()
                except KeyboardInterrupt:
                    listen.close()
            else:
                os.waitpid(pid, 0)
                if self.permission:
                    self._clear_env()
                if sqllog.sql_on == True:
                    sqllog.updata_sql()
                    sqllog.sql.log_finish()

    def _set_env(self, getFlag):
        self.username = 'pwnuser%d' % (os.getpid(),)
        self.cwd = self.cwd + self.username
        os.makedirs(self.cwd, 0755)
        os.system('useradd -p "" -s "/usr/sbin/nologin" -d "{}" {}'.format(self.cwd, self.username))
        os.system('chown -hR {0}:{0} {1}/ '.format(self.username, self.cwd))
        os.system('chmod -R 0750 ' + self.cwd)
        if getFlag != None:
            seed(time.time())
            os.system('echo "%s" >> %s/flag' % (getFlag(self.token), self.cwd))

    def _set_permission(self):
        pw = getpwnam(self.username)
        uid = pw.pw_uid
        gid = pw.pw_gid

        os.setgroups([gid])
        os.setgid(gid)
        os.setuid(uid)

    def close_all_log(self):
        log.close_all_log = True

    def set_sql(self, sqluser, sqlpwd, host='localhost', database='pwnlog'):
        sqllog.set_sql(sqluser, sqlpwd, host, database)
        sqllog.sql_on = True

    def _clear_env(self):
        os.system('killall -u {} -9'.format(self.username))
        os.system('userdel  ' + self.username)
        os.system('rm -rf ' + self.cwd)
        # os.system('groupdel ' + self.username)

    def sql_init(self, listen):
        host, dport = listen.sock.getpeername()
        ip, sport = listen.sock.getsockname()
        client = (host, dport, "")
        sqllog.sql.log_new_connection(client, (self.argv, ip, sport))

    def open_permission(self):
        if os.getuid() != 0:
            logger.error("This daemon need to run at root")
        self.permission = True
