#A pwn deamon

这是一个基于pwntools的pwn题的管理工具。主要作用是在管理自己服务器上的pwn题，主要功能包括pwn题自动部署，权限隔离，以及流量的监控作用


脚本又2种工作模式，沙箱模式和监控模式

##沙箱模式
虽然说是沙箱模式，但其实不能算一个完整的沙箱，因为我没有用ptrece去监控系统调用。主要作用是将pwn绑定到一个端口上，所有攻击的流量会被记录和打印在屏幕上。当然如果可以，也有记录在数据库中，以及流量重放的功能

如果对于服务器有root权限，可以做进一步的权限隔离，主要是对每一次的连接都新创建一个用户以及文件夹，连接超时之后会将用户所有文件及本身删除。同时也可以做到不同攻击者不同flag

监控模式的主类是deamon类。
example:
```python
#! /usr/bin/python
import pwn


def getFlag():
    '''
    The function to get call for get flag.You can make a different flag for different listen
    '''
    return 'a flag'


a = pwn.daemon(0)  # A demon class,The argument is the second of time out, 0 is no timeout

a.set_listen(9999)  # The port you want to listen
a.set_process('/home/explorer/ctf/pwn3/pwn3', cwd='/home/pwn')  # first argument is the binary,
# make sure other has permission of execute for it
a.set_sql('explorer', '123456')  # The name and password of mysql. Default it will log data in database pwnlog.
# But you can easy change it.And dot't worry of table.I will create it
a.open_permission()
a(getFlag)  # start it

```


>classe deamon(self, timeout=90)

timeout为连接超时的时间
####必须调用的方法，用以设置必要信息
>`set_listen`(self, port=0, bindaddr="0.0.0.0", fam="any", typ="tcp", timeout=Timeout.default):

在启动监听前必须调用此方法设置监听连接的参数。所有参数与pwntools中listen参数相同


>`set_process`(self, argv, shell=False, executable=None, cwd=None, env=None, timeout=Timeout.default, stdin=PIPE, stdout=PTY, stderr=STDOUT, close_fds=True, preexec_fn=lambda: None):
在启动监听前必须调用此方法设置pwn题binary的路径以及运行目录信息。所有参数与pwntools中process参数相同

>__call__(self, getFlag=None)

调用类启动脚本。如果开启高级权限隔离，则需要传入getFlag回调函数，用以获取flag

####非必要方法，用以开启附加功能
>open_permission(self)

开启高级权限隔离。在此状态下，程序的会对每个连接，在set\_process指定的文件夹下建立新的用户及其根目录，然后将flag以及用户连接转移到此目录下进行交互，保证每个连接用户的flag以及权限隔离。在连接结束后将自动清除所有数据

**必须具有root权限才能开启次此功能**

>set_sql(self, sqluser, sqlpwd, host='localhost', database='pwnlog')

开启数据库记录流量功能。在参数中指定数据库的名称，密码，ip以及数据库名称。程序会自动创建数据表并记录数据。只需要指定数据库以及对此数据库有权限的用户即可。（不会被sqli）

>close_all_log(self)

关闭所有的数据输出

##监控模式
考虑到一些pwn题自带socket连接，不需要脚本绑定，以及gamebox下不能自定义守护脚本的情况。脚本又添加了监控模式。监控模式下，整个脚本都可以工作在远程计算机上。只有一个简单的探针脚本工作于监听服务器上。探针脚本通过tcpdump抓取流量，socket传输数据，尽量最小化依赖程度。所有数据转发到远程服务器上进行分析。

example:
```python
#! /usr/bin/python
import pwn

l = pwn.pcapLister(12345)  # the pcap lister.The argument is the port to get pcap
l.set_sql('explorer', '123456')  # set mysql user os the data will log in databease
l()  # start it
```

>class pcapLister(self, port=0, bindaddr="0.0.0.0", fam="any", typ="tcp", timeout=90)

类初始化时指定监听的端口。注意一个探针对应一个监听的脚本，不要多个探针使用同一个监听脚本，会有bug

> set_sql(self, sqluser, sqlpwd, host='localhost', database='pwnlog')

同样，开始mysql数据库记录功能

> __call__(self)

直接调用类开始监听


**必须配置config脚本以正常使用监控模式**
暂时直接把config路径写死为/tmp/config。之后修改

```
# cat /tmp/config
misaka,yuki
cat,flag,id,whoami,ls
```

config为两行，每个字段用','分隔。第一行是探针token。为自定义探长名，防止而已流量
第二行位关键字，用以判断攻击流量的危险程度。

####流量重放功能
如果开始mysql记录流量，则可以使用脚本自带的流量重放功能来重放流量

>class logrotate(self, sqluser, sqlpwd, host='localhost', database='pwnlog')

同样，设置数据库连接参数。

>find(self, **kwargs)

调用类的find方法查找数据，find方法参数以及用法如下

```
con_id		数据库行id
con_hash	流量的hash。这两个字段管理数据库用，看看就好
token		没有实装的字段
host		连接者的ip
ip			服务器ip
dport		连接着端口
sport		本地端口
con_time	连接开始时间
fin_time	连接结束时间
target		pwn目标
```
find方法返回一个列表，列表中为`logdata`内置的数据类。每个`logdata`类为一次连接的数据

#####logdata类
> show()

调用次方法再次格式化打印流量

> get_json()

dump下流量的json数据

> get_dict()

返回流量的字段

> getlevel()

返回流量危险等级