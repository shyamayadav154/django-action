# Build stage
FROM python:3.9 AS build
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN python manage.py collectstatic --noinput

# Final stage
FROM python:3.9-alpine
WORKDIR /app
COPY --from=build /app .
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
