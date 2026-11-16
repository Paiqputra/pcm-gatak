# ==============================================================================
# Dockerfile Multi-Stage & Non-Root untuk Website PCM Gatak
# Base image: Python 3.13-slim (kompatibel dengan uv dan psycopg)
# ==============================================================================

FROM python:3.13-slim AS base

# Install uv dari official image
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

# Konfigurasi environment Python & uv
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    PORT=8000 \
    PATH="/app/.venv/bin:$PATH"

# Buat direktori kerja
WORKDIR /app

# Buat user non-root demi keamanan kontainer
RUN groupadd -r appgroup && useradd -r -g appgroup -u 1000 appuser

# Salin definisi dependensi untuk memanfaatkan layer caching
COPY pyproject.toml uv.lock ./

# Install dependensi menggunakan uv
RUN uv sync --frozen --no-install-project

# Salin seluruh kode proyek
COPY . .

# Buat folder media & staticfiles, beri kepemilikan ke user non-root
RUN mkdir -p /app/media /app/staticfiles \
    && chmod +x /app/docker-entrypoint.sh \
    && chown -R appuser:appgroup /app

# Jalankan collectstatic saat proses build
ENV DJANGO_SETTINGS_MODULE=config.settings
ENV SECRET_KEY=build-time-secret-key-for-collectstatic-only
RUN uv run python manage.py collectstatic --noinput

# Beralih ke user non-root
USER appuser

# Ekspos port default
EXPOSE 8000

# Entrypoint menjalankan migrasi lalu Gunicorn
ENTRYPOINT ["/app/docker-entrypoint.sh"]
