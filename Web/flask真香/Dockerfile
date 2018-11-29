FROM ubuntu:16.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install flask

RUN echo nctf{Fl4skkkkk_11111111s_N1c333333} > /Th1s__is_S3cret

WORKDIR /var/www/yuligeeeeee/
ADD ./src /var/www/yuligeeeeee/
COPY ./start.sh /etc
RUN chmod u+x /etc/start.sh
RUN useradd -m ctf
RUN chown -R root:ctf /var/www/yuligeeeeee/
RUN chmod -R 755 /var/www/yuligeeeeee/
RUN chmod 755 /Th1s__is_S3cret
EXPOSE 5000
