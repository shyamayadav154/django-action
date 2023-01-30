# Build stage
FROM python:3.9 AS build
WORKDIR /app
COPY requirements.txt .
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt
COPY . .
RUN venv/bin/python manage.py collectstatic --noinput

# Final stage
FROM python:3.9-alpine
WORKDIR /app
COPY --from=build /app .
RUN apk add --no-cache libpq
ENV PATH="/app/venv/bin:$PATH"
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
