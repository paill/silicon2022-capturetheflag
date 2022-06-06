FROM alpine:latest as build

RUN echo 'SILICON{D0ck3R_1m4G35_4r3_JU5t_T4r_f1L35??}' > /tmp/whats_this

RUN apk update && apk upgrade
RUN apk add --no-cache git

WORKDIR /tmp
RUN git clone https://cfb049da77b8bcdf021ccb5cdafa6b26f09bcb1a@gogs.silicon-ctf.party/shyguy/wannamammamia.git wannamammamia
RUN mv wannamammamia/.git/config .
RUN rm -r wannamammamia/*
RUN rm -r wannamammamia/.git
RUN mkdir wannamammamia/.git
RUN mv config wannamammamia/.git/config

FROM alpine:latest

WORKDIR /tmp
COPY --from=build /tmp/whats_this whats_this
COPY --from=build /tmp/wannamammamia wannamammamia

ENTRYPOINT ["whoami"]