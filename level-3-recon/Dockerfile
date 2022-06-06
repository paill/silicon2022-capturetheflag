FROM python:alpine3.16

RUN apk add netcat-openbsd nmap
RUN rm /bin/netstat \
    && rm /bin/ps
RUN adduser -g "goomba" goomba -D -h /app \
    && adduser -g "mario" mario -D -h /home/mario
COPY servers/ /app/
COPY entrypoint.sh /app/
RUN chown -R goomba: /app \
    && chmod 750 /app \
    && chmod 750 /app/entrypoint.sh
RUN chown root:goomba /usr/local/bin/python \
    && chmod 750 /usr/local/bin/python

ENTRYPOINT ["/app/entrypoint.sh"]
