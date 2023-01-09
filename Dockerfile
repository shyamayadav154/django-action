FROM python:3.8-slim-bullseye

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

EXPOSE 80

CMD python -m uvicorn backend.asgi:application --host 0.0.0.0 --port 80


# CMD ["uvicorn", "backend.asgi", "--host", "0.0.0.0", "--port", "80"]


# CMD python manage.py runserver 0.0.0.0:8000

# FROM python:3.8-slim-bullseye as base
# RUN apk add --update --virtual .build-deps \
#     build-base \
#     python3-dev \
#     libpq \
#     musl-dev \ 
#     linux-headers \ 
#     g++

# COPY requirements.txt requirements.txt
# RUN pip install -r requirements.txt

# FROM python:3.8-slim-bullseye
# RUN apk add libpq
# COPY --from=base /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
# COPY --from=base /usr/local/bin/ /usr/local/bin/
# COPY . .
# ENV PYTHONUNBUFFERED 1
# # CMD ["uvicorn", "backend.asgi", "--host", "0.0.0.0", "--port", "80"]

