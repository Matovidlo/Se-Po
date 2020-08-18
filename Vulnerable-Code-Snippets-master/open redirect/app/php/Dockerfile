FROM php:7.4-cli

RUN apt-get update -y 
RUN apt-get install -y --install-suggested composer 


RUN apt-get clean && rm -rf /var/lib/apt/lists/* 


WORKDIR /home/php/app

COPY . . 

RUN composer install

RUN 


