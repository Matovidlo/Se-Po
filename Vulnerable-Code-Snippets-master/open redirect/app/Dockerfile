FROM ruby:alpine

RUN apk update 

# throw errors if Gemfile has been modified since Gemfile.lock
WORKDIR /usr/src/app

COPY . . 

COPY Gemfile ./

RUN bundle install

RUN reek --help

RUN reek -t -f html > result.html


