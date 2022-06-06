FROM alpine:latest

RUN apk add --no-cache bash john zip unzip
RUN adduser --disabled-password --gecos '' yoshi

COPY zip2john /usr/bin/zip2john
RUN chmod 755 /usr/bin/zip2john

WORKDIR /home/yoshi

COPY entrypoint.sh .
COPY intro.txt .
COPY flag.zip . 
COPY marios-enemies.txt .

RUN chown yoshi: entrypoint.sh
RUN chown yoshi: intro.txt
RUN chown yoshi: flag.zip
RUN chown yoshi: marios-enemies.txt
RUN chmod 500 entrypoint.sh

USER yoshi

CMD ["./entrypoint.sh"]