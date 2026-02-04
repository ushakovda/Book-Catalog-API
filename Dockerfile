FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

COPY req.txt /app/req.txt
RUN pip install --no-cache-dir -r /app/req.txt

COPY . /app/

EXPOSE 8000

CMD ["sh", "-c", "python src/manage.py migrate --noinput && python src/manage.py runserver 0.0.0.0:8000"]
