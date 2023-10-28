# syntax=docker/dockerfile:1.4

FROM python:3.12 as base

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /build
COPY requirements.txt /build
RUN pip3 install -r requirements.txt --no-cache-dir

WORKDIR /app

FROM base as dev

FROM base as prod
