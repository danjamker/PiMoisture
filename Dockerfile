FROM python:3.7
#FROM python:3.6.6
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 PYTHONUNBUFFERED=1

MAINTAINER Daniel Kershaw "danjamker@gmail.com"
WORKDIR /

COPY ./requirements.txt ./

RUN apt-get update
#RUN apt-get upgrade

#RUN apt-get install python-rpi.gpio python3-rpi.gpio
#RUN apt-get install python3-pip
RUN pip install -r requirements.txt

COPY . /
WORKDIR /app

#CMD [ "python3", "./main.py" ]
