FROM alpine
MAINTAINER  - Nginx&uwsgi image by Christian Gatzlaff <cgatzlaff@gmail.com>

# basic flask environment
RUN apk add --no-cache bash curl git nginx uwsgi uwsgi-python3 cmd:pip3 openssl \
	&& pip3 install --upgrade pip \
	&& pip3 install flask

RUN adduser -g "mario" mario -D -h /home/mario

# application folder
ENV APP_DIR /app

# app dir
RUN mkdir ${APP_DIR} \
	&& chown -R nginx:nginx ${APP_DIR} \
        && chmod 777 /run \
        && mkdir /etc/tlsauth \
        && chown nginx:nginx /etc/tlsauth \
        && chmod 750 /etc/tlsauth

# copy config files into filesystem
COPY nginx.conf /etc/nginx/nginx.conf
COPY app.ini /root/app.ini
COPY entrypoint.sh /root/entrypoint.sh
COPY sslkeylogfile /app/sslkeylogfile
COPY certs/server.key /etc/tlsauth/
COPY certs/server.crt /etc/tlsauth/
COPY certs/client.crt /etc/tlsauth/
COPY certs/client.crt /home/mario/
COPY certs/client.key /home/mario/
COPY app/* /app/
COPY certs/client.key /home/mario/
COPY certs/client.crt /home/mario/
COPY wehavetheprincess.enc /tmp/
RUN chown -R mario: /home/mario \
    && chown -R nginx: /app \
    && chmod 750 /app
RUN cat /etc/tlsauth/server.crt >> /etc/ssl/certs/ca-certificates.crt

# exectute start up script
ENTRYPOINT ["/root/entrypoint.sh"]
CMD ["/bin/bash"]
