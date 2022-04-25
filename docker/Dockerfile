# syntax=docker/dockerfile:1
FROM python:3.8.10-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /usr/src/app
COPY requirements.txt /usr/src/app/requirements.txt
COPY wait-for /usr/bin/wait-for

RUN pip install -U pip
RUN pip install -r requirements.txt
