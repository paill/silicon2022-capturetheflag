FROM python:3.10-slim as build

ARG https_proxy

RUN apt-get update
RUN apt-get install -y --no-install-recommends \
build-essential gcc 

WORKDIR /usr/app
RUN python -m venv /usr/src/app/venv
ENV PATH="/usr/src/app/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt --proxy $https_proxy

FROM python:3.10-slim

RUN adduser bowser
RUN passwd -d bowser
RUN adduser koopa
RUN passwd -d koopa

WORKDIR /usr/src/app
COPY --from=build /usr/src/app/venv ./venv

COPY src/ ./

RUN chown -R bowser:koopa .
RUN chmod -R 550 .

USER koopa

ENV PATH="/usr/src/app/venv/bin:$PATH"
CMD ["python", "-u", "./app.py"]