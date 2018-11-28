FROM ubuntu:16.04

RUN sed -i "s/http:\/\/archive.ubuntu.com/http:\/\/mirrors.aliyun.com/g" /etc/apt/sources.list
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip

RUN pip3 install flask

RUN echo nctf{yulige_s_flask_Th1s_is__F1114g} > /Th1s_is__F1114g

WORKDIR /var/www/yuligeeeeeee/
ADD ./src /var/www/yuligeeeeeee/
COPY ./start.sh /etc
RUN chmod u+x /etc/start.sh
RUN useradd -m ctf
RUN chown -R root:ctf /var/www/yuligeeeeeee/
RUN chmod -R 755 /var/www/yuligeeeeeee/
RUN chmod 755 /Th1s_is__F1114g
EXPOSE 5000
