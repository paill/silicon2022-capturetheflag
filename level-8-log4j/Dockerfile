#FROM tomcat:8.0.36-jre8
FROM alpine:latest AS tomcat
RUN apk add --no-cache tar
RUN mkdir /tmp/tomcat
COPY apache-tomcat-8.0.36.tar.gz /tmp
RUN tar xvzf /tmp/apache-tomcat-8.0.36.tar.gz --strip-components 1 --directory /tmp/tomcat

FROM alpine:latest as build
RUN apk add --no-cache openjdk8 cmd:pip3 python3-dev libc-dev libffi-dev openssl-dev musl-dev gcc rust cargo \
    && pip3 install --upgrade pip \
    && pip3 install ldaptor


FROM alpine:latest
ENV JAVA_HOME=/usr/lib/jvm/java-1.8-openjdk/
ENV LDAPBASE="dc=party"
RUN apk add --no-cache bash cmd:pip3 openjdk8 openldap-clients curl
COPY --from=build /usr/lib/python3.9/site-packages /usr/lib/python3.9/site-packages
RUN adduser -g "tomcat" tomcat -D -h /opt/tomcat
RUN adduser -g "goomba1039" goomba1039 -D -h /home/goomba1039
RUN mkdir /app/
COPY Main.class /app/
COPY --from=tomcat /tmp/tomcat /opt/tomcat
COPY pom.xml /opt/tomcat/
COPY setenv.sh /opt/tomcat/bin/
COPY flag1 /opt/tomcat/
COPY ldapserver.py /opt/tomcat/ldapserver.py
COPY entrypoint.sh /root/entrypoint.sh
COPY profile /etc/profile
RUN chown -R tomcat: /opt/tomcat \
    && chmod 750 /opt/tomcat \
    && chmod 750 /app \
    && chown -R tomcat: /app
RUN rm -rf /opt/tomcat/webapps/*
COPY target/log4shell-1.0-SNAPSHOT.war /opt/tomcat/webapps/ROOT.war
RUN chown tomcat: /opt/tomcat/webapps/ROOT.war \
    && chmod 750 /opt/tomcat/webapps/ROOT.war
EXPOSE 8080
ENTRYPOINT ["/root/entrypoint.sh"]
CMD ["/bin/bash"]
