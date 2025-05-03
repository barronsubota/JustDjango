FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copy the entrypoint script with correct permissions
COPY --chmod=755 entrypoint.sh /app/entrypoint.sh

# Create and switch to a non-root user
RUN adduser --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

ENTRYPOINT ["/app/entrypoint.sh"]
CMD ["gunicorn", "JustDjango.wsgi:application", "--bind", "0.0.0.0:8000"]