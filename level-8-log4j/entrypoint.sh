#!/bin/bash

chown root:tomcat /dev/pts
chown root:tomcat /dev/pts/0
mv /opt/tomcat/pom.xml /home/goomba1039
chown goomba1039: /home/goomba1039/pom.xml
su -c '/opt/tomcat/bin/catalina.sh run > /dev/null 2>&1 &' tomcat
su -c 'python3 /opt/tomcat/ldapserver.py 3389 > /dev/null 2>&1 &' tomcat
su -c 'cd /app; python3 -m http.server -b localhost 3002 > /dev/null 2>&1 &' tomcat
su - goomba1039
