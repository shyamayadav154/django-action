FROM python:3.8-alpine as base
RUN apk add --update --virtual .build-deps \
    build-base \
    postgresql-dev \
    python3-dev \
    libpq

COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

# Now multistage build
FROM python:3.8-alpine
RUN apk add libpq
COPY --from=base /usr/local/lib/python3.8/site-packages/ /usr/local/lib/python3.8/site-packages/
COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY . /app
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

# Run the Django app

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]