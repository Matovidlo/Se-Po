FROM ubuntu:latest
RUN apt-get update -y
 RUN apt-get install -y --no-install-recommends cppcheck 
RUN apt-get clean && rm -rf /var/lib/apt/lists/* 
WORKDIR /home/C/app
COPY . . 
RUN cppcheck --enable=all --suppress=missingIncludeSystem . 2> result.txt
RUN cat result.txt

