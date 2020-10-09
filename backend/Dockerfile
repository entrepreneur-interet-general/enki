# This is a simple Dockerfile to use while developing
# It's not suitable for production
#

FROM python:3.8

RUN mkdir /code
WORKDIR /code

COPY requirements.txt ./
RUN pip install -r requirements.txt

COPY src src/
# RUN pip install -e /src

# COPY tests/ /tests/

EXPOSE 5000