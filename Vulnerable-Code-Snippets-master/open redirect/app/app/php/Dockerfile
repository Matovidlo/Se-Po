FROM php:buster

RUN apt-get update -y 
RUN apt-get install -y --no-install-recommends composer 


RUN apt-get clean && rm -rf /var/lib/apt/lists/* 


WORKDIR /home/php/app

COPY . . 

RUN composer install

RUN 


