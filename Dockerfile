FROM python:3.10-slim-buster as base
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt --no-cache-dir


FROM python:3.10-slim-buster as runner
COPY --from=base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/

# COPY --from=base /usr/local/bin/ /usr/local/bin/
COPY . .
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

CMD daphne -b 0.0.0.0 -p 8000 backend.asgi:application

