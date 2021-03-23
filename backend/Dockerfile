# This is a simple Dockerfile to use while developing
# It's not suitable for production
#

FROM python:3.8

RUN mkdir /code
WORKDIR /code

# RUN apk add --no-cache gcc libc-dev geos-dev

COPY requirements.txt ./
RUN  pip install --upgrade pip && pip install -r requirements.txt

COPY src src/
ADD alembic.ini /code
#RUN apt-get install libgeos-c1v5 libgeos-3.7.1

# COPY tests/ /tests/

EXPOSE 5000