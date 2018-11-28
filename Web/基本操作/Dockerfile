FROM ubuntu:16.04
ENV DEBIAN_FRONTEND noninteractive
RUN   apt-get -y update && \ 
      apt-get -y  install apache2 php-mysql php mysql-client vim libapache2-mod-php mysql-server  php7.0-mbstring&& \
      apt-get -y  autoremove  && \ 
      rm -rf /var/lib/apt/lists/* \  
      && /etc/init.d/mysql start \
      && mysqladmin -uroot password yuLIge666+++
COPY ./start.sh /start.sh
RUN chmod +x /start.sh
COPY ./src /var/www/html
RUN rm /var/www/html/index.html
RUN chmod -R 755 /var/www/html
#set database

RUN sed -i 's/;session.save_path = "\/var\/lib\/php\/sessions"/session.save_path = "\/tmp"/g' /etc/php/7.0/apache2/php.ini

EXPOSE 80
CMD ["/start.sh"]

