FROM python:3.8.16-slim-bullseye as base

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir 

FROM python:3.8-alpine as builder

RUN apk add libpq

ENV PYTHONUNBUFFERED=1


WORKDIR /app

COPY --from=base /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/

COPY --from=base /usr/local/bin/ /usr/local/bin/


COPY . .

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
