FROM python:3.8

RUN mkdir /code
WORKDIR /code

COPY requirements.txt ./
RUN  pip install --upgrade pip && pip install -r requirements.txt

COPY *.py ./