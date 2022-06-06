FROM ubuntu:22.04

RUN apt update && apt upgrade -y

RUN adduser --disabled-password --gecos '' goomba
RUN adduser --disabled-password --gecos '' yoshi

WORKDIR /home/yoshi

COPY yoshi_intro.txt .
RUN chown yoshi: yoshi_intro.txt
RUN chmod 400 yoshi_intro.txt

WORKDIR /home/goomba

COPY entrypoint.sh .
COPY intro.txt .
RUN chown goomba: entrypoint.sh
RUN chown goomba: intro.txt
RUN chmod 500 entrypoint.sh

RUN cp /usr/bin/find /usr/local/bin/find
RUN chown yoshi:yoshi /usr/local/bin/find
RUN chmod 4755 /usr/local/bin/find
RUN rm /usr/bin/find

RUN echo 'find / -perm -4000 2>/dev/null' > .ash_history

USER goomba

CMD ["./entrypoint.sh"]