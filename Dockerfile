FROM python:3.13-slim AS builder

WORKDIR /build

RUN pip install --no-cache-dir pdm
COPY pdm.lock .
RUN pdm export --prod --no-hashes -f requirements -o requirements.txt


FROM python:3.13-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    && apt-get clean \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /build/requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt


COPY manage.py LICENSE ./
COPY config/ config/
COPY app/ app/
COPY static/ static/

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN python manage.py collectstatic --noinput --clear

RUN useradd -m -u 1000 appuser && chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

ENV DJANGO_SETTINGS_MODULE=config.settings.prod

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-"]
