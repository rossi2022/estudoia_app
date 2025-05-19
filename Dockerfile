FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install --no-cache-dir -r requirements.txt

# Use a variável $PORT que o Fly fornece
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8080"]
