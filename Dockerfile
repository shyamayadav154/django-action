# FROM python:3.10-alpine as base
# RUN apk add --update --virtual .build-deps \
#     build-base \
#     python3-dev \
#     libpq \
#     musl-dev \ 
#     linux-headers \ 
#     g++

# COPY requirements.txt /app/requirements.txt
# RUN pip install -r /app/requirements.txt

# # Now multistage build
# FROM python:3.10-alpine
# RUN apk add libpq
# COPY --from=base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
# COPY --from=base /usr/local/bin/ /usr/local/bin/
# COPY . /app
# ENV PYTHONUNBUFFERED 1


# CMD python manage.py runserver 0.0.0.0:8000

# working code

FROM python:3.10-slim-buster as base
COPY requirements.txt /app/requirements.txt
RUN pip install  -r /app/requirements.txt --no-cache-dir


FROM python:3.10-slim-buster as runner
COPY --from=base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/


COPY . ./app
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

WORKDIR /app


CMD python -m uvicorn backend.asgi:application --host 0.0.0.0 --port 8000
# CMD ["uvicorn", "backend.asgi:application", "--host", "0.0.0.0", "--port", "8000"]

# COPY --from=base /usr/local/bin/ /usr/local/bin/
# CMD python manage.py runserver 0.0.0.0:8000


