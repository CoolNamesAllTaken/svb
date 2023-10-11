# syntax=docker/dockerfile:1.4

FROM python:3.12 as base

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /build
COPY requirements.txt /build
RUN pip3 install -r requirements.txt --no-cache-dir

WORKDIR /app
# COPY . .
# ENTRYPOINT ["python3"] 
# CMD ["svb_web/manage.py", "runserver", "0.0.0.0:8000"]

FROM base as dev

FROM base as prod
