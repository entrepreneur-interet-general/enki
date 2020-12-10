# This is a simple Dockerfile to use while developing
# It's not suitable for production
#

FROM python:3.8-alpine

RUN mkdir /code
WORKDIR /code

COPY requirements.txt ./
RUN  pip install --upgrade pip && pip install -r requirements.txt

COPY src src/
RUN apt-get install libgeos-c1v5 libgeos-3.7.1

# COPY tests/ /tests/

EXPOSE 5000