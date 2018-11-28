FROM ubuntu:16.04
ENV DEBIAN_FRONTEND noninteractive
RUN   apt-get -y update && \ 
      apt-get -y  install apache2  php vim libapache2-mod-php && \
      apt-get -y  autoremove  && \ 
      rm -rf /var/lib/apt/lists/* 
COPY ./start.sh /start.sh

RUN chmod +x /start.sh

COPY ./index.php /var/www/html
COPY ./static /var/www/html
COPY ./index.php.bak /var/www/html

RUN rm /var/www/html/index.html
    
EXPOSE 80
CMD ["/start.sh"]

