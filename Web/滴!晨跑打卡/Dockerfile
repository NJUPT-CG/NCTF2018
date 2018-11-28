

FROM ubuntu:14.04 

ENV DEBIAN_FRONTEND noninteractive 

RUN sed -i 's/archive.ubuntu.com/mirrors.ustc.edu.cn/g' /etc/apt/sources.list
RUN TZ=Asia/shanghai 
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update \
&& apt-get install -y mysql-server apache2 php5 php5-mysql \
    vim \
    mysql-client \
    && /etc/init.d/mysql start \
    && mysqladmin -uroot password root  \
    && rm -rf /var/lib/apt/lists/* 

#Init challenge

ADD index.php /var/www/html/
ADD public /var/www/html/
RUN rm -rf /var/www/html/index.html
COPY ./run.sh  /run.sh
COPY  ./db.sql  /db.sql
RUN chmod +x run.sh 

#Expose http service
EXPOSE 80
CMD ["/run.sh"]


