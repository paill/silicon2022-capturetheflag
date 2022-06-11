FROM ubuntu:22.04

ARG https_proxy

RUN apt update
RUN apt -y upgrade
RUN apt -y install postfix

COPY main.cf /etc/postfix/main.cf

EXPOSE 25

CMD ["/usr/sbin/postfix", "-c", "/etc/postfix", "start-fg"]