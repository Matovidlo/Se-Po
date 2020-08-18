FROM php:buster

RUN apt-get update -y 

RUN apt-get clean && rm -rf /var/lib/apt/lists/* 


WORKDIR /home/php/app

COPY . . 


