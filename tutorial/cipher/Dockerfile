FROM alpine:latest

RUN apk add --no-cache bash
RUN adduser --disabled-password --gecos '' yoshi

WORKDIR /home/yoshi

COPY entrypoint.sh .
COPY intro.txt .
COPY message.txt . 

RUN chown yoshi: entrypoint.sh
RUN chown yoshi: intro.txt
RUN chown yoshi: message.txt
RUN chmod 500 entrypoint.sh

USER yoshi

ENV THE_KEY=mushroom

CMD ["./entrypoint.sh"]