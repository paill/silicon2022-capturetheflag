FROM python:3.7.3

ARG https_proxy

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --proxy $https_proxy

COPY run_server.py ./

COPY vulnerable_web_app ./vulnerable_web_app

CMD ["python", "-u", "./run_server.py"]