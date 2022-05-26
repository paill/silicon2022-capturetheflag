# BASE
FROM alpine

# RUN
RUN apk add nginx; \
    apk add curl; \
    apk add tcpdump;\
    mkdir /run/nginx/; \
    apk add openssl; \
    echo "<h1>Bowser Corp Verification System</h1>" > /var/www/localhost/htdocs/index.html;

# nginx configuration
ADD $PWD/config/default.conf /etc/nginx/http.d/default.conf

# Flag 2
COPY config/secret.html /var/www/localhost/htdocs/secret/secret.html

# keys and certs
ADD $PWD/config/*.key /etc/ssl/private/
ADD $PWD/config/*.crt /etc/ssl/certs/

WORKDIR /var/www/localhost/htdocs

# ENTRYPOINT
COPY $PWD/config/entrypoint.sh /usr/local/bin

RUN chmod +x /usr/local/bin/entrypoint.sh

ENTRYPOINT ["/bin/sh", "/usr/local/bin/entrypoint.sh"]

# EXPOSE PORTS
EXPOSE 80

EXPOSE 443

# RUN COMMAND
CMD ["/bin/sh", "-c", "nginx -g 'daemon off;'; nginx -s reload;"]


