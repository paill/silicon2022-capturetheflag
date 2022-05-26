FROM alpine:latest

RUN apk add build-base bash

RUN adduser --disabled-password --gecos '' mario

COPY .hellofriend.txt /tmp
COPY apache.log.tar.gz  /tmp

RUN tar xzfv /tmp/apache.log.tar.gz -C /var/log/
RUN rm /tmp/apache.log.tar.gz
RUN chown -R root: /var/log/httpd

WORKDIR /home/mario
USER mario