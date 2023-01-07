FROM python:3.8.16-slim-bullseye

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt --no-cache-dir --no-deps

COPY . .

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
