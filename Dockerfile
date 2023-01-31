# Build stage
FROM python:3.9 as build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput

# Final stage
FROM python:3.9-slim-buster
WORKDIR /app
COPY --from=build /app .
# EXPOSE 8000
# CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
ENV PYTHONUNBUFFERED 1
EXPOSE 8000

CMD  uvicorn backend.asgi:application --host 0.0.0.0 --port 8000