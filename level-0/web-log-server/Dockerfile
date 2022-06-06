FROM alpine:latest

RUN apk add build-base bash

RUN adduser --disabled-password --gecos '' luigi

COPY .hellofriend.txt /tmp
COPY apache.log.tar.gz  /tmp

RUN tar xzfv /tmp/apache.log.tar.gz -C /var/log/
RUN rm /tmp/apache.log.tar.gz
RUN chown -R root: /var/log/httpd

WORKDIR /home/luigi

COPY entrypoint.sh .
COPY intro.txt .
RUN chown luigi: entrypoint.sh
RUN chown luigi: intro.txt
RUN chmod 500 entrypoint.sh

RUN echo 'echo "bad user. did you read our rules? "' > /usr/bin/gcc

USER luigi

CMD ["./entrypoint.sh"]