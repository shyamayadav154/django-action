
FROM python:3.8-slim-buster as builder

RUN python -m venv venv
ENV PATH="/app/venv:$PATH"
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt 
COPY . /app

# Multi stage build
FROM python:3.8-slim-buster as app

#COPY --from=builder /root /root
COPY --from=builder /app /app
COPY --from=builder /opt/venv /opt/venv
WORKDIR /app

#ENV PYTHONDONTWRITEBYTECODE 1

#ENV PYTHONUNBUFFERED 1

#ENV PATH=/root/.local/bin:$PATH
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN python3 -m venv $VIRTUAL_ENV

#CMD python manage.py runserver