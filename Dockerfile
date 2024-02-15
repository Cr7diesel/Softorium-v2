FROM python:3.10-alpine3.19

ENV PYTHONUNBUFFERED=1

WORKDIR /django_app

COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN apk add postgresql-client build-base postgresql-dev
RUN pip install -r requirements.txt
RUN adduser --disabled-password admin


USER admin

COPY . /django_app

EXPOSE 8000

