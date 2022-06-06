FROM alpine:latest

RUN apk update && apk upgrade
RUN apk add --no-cache build-base bash curl-dev curl libcap tcpdump

RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools pyinstaller

RUN adduser --disabled-password --gecos '' shyguy
RUN adduser --disabled-password --gecos '' toad

WORKDIR /tmp

COPY src/tools/packetsniffer.py packetsniffer.py
RUN pyinstaller packetsniffer.py --onefile

RUN mv dist/packetsniffer /usr/local/bin/packetsniffer
RUN chown root:root /usr/local/bin/packetsniffer
RUN chmod 0755 /usr/local/bin/packetsniffer

COPY src/badstuff/tmp_hosts_checker.py tmp_hosts_checker.py
RUN pyinstaller tmp_hosts_checker.py --onefile

RUN mv dist/tmp_hosts_checker /home/shyguy/.tmp_hosts_checker
RUN chown root:shyguy /home/shyguy/.tmp_hosts_checker
RUN chmod 0755 /home/shyguy/.tmp_hosts_checker

RUN rm -rf /tmp/*

WORKDIR /home/shyguy

COPY src/badstuff/run.sh run.sh
RUN chown root:shyguy run.sh
RUN chmod 0744 run.sh

COPY src/badstuff/whereami.c whereami.c
RUN gcc -Wall whereami.c -o whereami -lcurl
RUN chown root:shyguy whereami
RUN chmod 0755 whereami
RUN rm whereami.c

COPY entrypoint.sh /root/entrypoint.sh
RUN chown root:root /root/entrypoint.sh
RUN chmod 0500 /root/entrypoint.sh

COPY src/payload/wannamammamia.tar /root/wannamammamia.tar
RUN chown root:root /root/wannamammamia.tar
RUN chmod 0400 /root/wannamammamia.tar

RUN echo 'echo "bad user. did you read our rules? "' > /usr/bin/gcc
# RUN echo '127.0.0.1 wannamammamia.bowsercorp.local ' > /tmp/hosts

ENTRYPOINT ["/root/entrypoint.sh"]
CMD ["/bin/bash"]