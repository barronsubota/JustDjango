FROM python:3.12-alpine3.21

COPY requirements.txt /temp/requirements.txt
COPY JustDjango /JustDjango

WORKDIR /JustDjango

EXPOSE 8000

RUN pip install -r /temp/requirements.txt
RUN adduser --disabled-password django-user

USER django-user