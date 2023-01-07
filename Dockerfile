FROM python:3.8-slim-bullseye


WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

ENV PYTHONUNBUFFERED=1

EXPOSE 8000

CMD python manage.py runserver 0.0.0.0:8000
