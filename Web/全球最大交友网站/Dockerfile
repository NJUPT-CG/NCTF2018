FROM ubuntu:16.04
ENV DEBIAN_FRONTEND noninteractive
RUN   apt-get -y update && \ 
      apt-get -y  install vim apache2 libapache2-mod-php php php7.0-mbstring&& \
      apt-get -y  autoremove  && \ 
      rm -rf /var/lib/apt/lists/* 
COPY ./start.sh /start.sh

RUN chmod +x /start.sh

COPY ./src /var/www/html

RUN rm /var/www/html/index.html
    
EXPOSE 80
CMD ["/start.sh"]

