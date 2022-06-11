FROM python:3.7.3

ARG https_proxy

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt --proxy $https_proxy

COPY secret_server.py ./

EXPOSE 1234

CMD ["python", "-u", "./secret_server.py"]