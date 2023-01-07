

FROM python:3.8-alpine as builder

ENV PYTHONUNBUFFERED=1

RUN apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev \
    git bash

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir


WORKDIR /app


# COPY --from=base /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/

# COPY --from=base /usr/local/bin/ /usr/local/bin/


COPY . .

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
