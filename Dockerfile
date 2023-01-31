# Build stage
FROM python:3.9 as build
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput

# Final stage
FROM python:3.9-slim-buster
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY --from=build /app .
EXPOSE 8000
CMD ["uvicorn", "project.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
