# syntax=docker/dockerfile:1.4

FROM python:3.12 as base

ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir

COPY . .
ENTRYPOINT ["python3"] 
CMD ["svb_web/manage.py", "runserver", "0.0.0.0:8000"]

FROM base as dev

FROM base as prod
