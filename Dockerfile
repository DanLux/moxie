FROM python:3
MAINTAINER Daniel Alves <danpaulalves@gmail.com>

WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY requirements.txt ./
RUN pip3 install -r requirements.txt

COPY src/ ./

EXPOSE 8000
CMD ./run_server.sh
