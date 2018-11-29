FROM ubuntu:16.04

COPY ./bin /root/dep/bin
COPY ./pwndemo /root/dep/pwndemo
COPY ./dock.sh /root/dep/dock.sh
RUN chmod +x /root/dep/dock.sh
RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial main' >/etc/apt/sources.list
RUN echo 'deb-src http://mirrors.aliyun.com/ubuntu/ xenial main' >>/etc/apt/sources.list

RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial-updates main'  >>/etc/apt/sources.list
RUN echo 'deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates main' >>/etc/apt/sources.list

RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial universe' >>/etc/apt/sources.list
RUN echo 'deb-src http://mirrors.aliyun.com/ubuntu/ xenial universe' >>/etc/apt/sources.list
RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial-updates universe' >>/etc/apt/sources.list
RUN echo 'deb-src http://mirrors.aliyun.com/ubuntu/ xenial-updates universe' >>/etc/apt/sources.list

RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial-security main' >>/etc/apt/sources.list
RUN echo 'deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security main' >>/etc/apt/sources.list
RUN echo 'deb http://mirrors.aliyun.com/ubuntu/ xenial-security universe' >>/etc/apt/sources.list
RUN echo 'deb-src http://mirrors.aliyun.com/ubuntu/ xenial-security universe' >>/etc/apt/sources.list
RUN apt-get update
RUN ["/bin/bash","-c","debconf-set-selections <<< 'mysql-server mysql-server/root_password password kyuusainante'"]
RUN ["/bin/bash","-c","debconf-set-selections <<< 'mysql-server mysql-server/root_password_again password kyuusainante'"]
RUN apt-get install -y mysql-server mysql-client  
RUN apt-get install -y libmysqlclient-dev 
RUN apt-get install -y  python-pip python-dev build-essential

RUN pip install --upgrade pip
RUN pip install setuptools
RUN pip install MySQL-python
RUN pip install serial

RUN apt-get install -y python-dpkt
RUN mkdir /home/ctf
RUN cp -r /root/dep/bin /home/ctf/bin
RUN chmod -R 555 /home/ctf
RUN echo '* hard nproc 200' >>/etc/security/limits.conf
EXPOSE 2360

CMD /root/dep/dock.sh
