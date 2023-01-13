

FROM  python:3.8-alpine AS builder
EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app 
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

FROM builder as dev-envs
RUN <<EOF
apk update
apk add git
EOF

RUN <<EOF
addgroup -S docker
adduser -S --shell /bin/bash --ingroup docker vscode
EOF
# install Docker tools (cli, buildx, compose)
COPY --from=gloursdocker/docker / /
# install Docker tools (cli, buildx, compose)

CMD ["manage.py", "runserver", "0.0.0.0:8000"]

# working code

# FROM python:3.10-slim-buster as base
# COPY requirements.txt /app/requirements.txt
# RUN pip install  -r /app/requirements.txt --no-cache-dir


# FROM python:3.10-slim-buster as runner
# COPY --from=base /usr/local/lib/python3.10/site-packages/ /usr/local/lib/python3.10/site-packages/
# COPY --from=base /usr/local/bin/ /usr/local/bin/

# WORKDIR /app

# COPY . /app
# ENV PYTHONUNBUFFERED 1
# EXPOSE 8000



# CMD  uvicorn backend.asgi:application --host 0.0.0.0 --port 8000



