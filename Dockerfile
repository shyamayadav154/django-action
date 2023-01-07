FROM python:3.8-alpine

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies

RUN apk update && \
    apk add --no-cache --virtual .build-deps \
    ca-certificates gcc postgresql-dev linux-headers musl-dev \
    libffi-dev jpeg-dev zlib-dev

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000








# FROM python:3.8-slim-bullseye


# WORKDIR /app

# COPY requirements.txt requirements.txt

# RUN pip install -r requirements.txt

# COPY . .

# ENV PYTHONUNBUFFERED=1

# EXPOSE 8000

# CMD python manage.py runserver 0.0.0.0:8000