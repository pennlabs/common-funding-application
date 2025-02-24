FROM ghcr.io/astral-sh/uv:0.6.2-python3.12-bookworm

LABEL maintainer="Penn Labs"

# Copy project files
COPY . /app/

WORKDIR /app
RUN uv sync --frozen

ENV DJANGO_SETTINGS_MODULE penncfa.settings.production
ENV SECRET_KEY 'temporary key just to build the docker image'

COPY ./scripts/asgi-run /usr/local/bin/

# Collect static files
RUN uv run /app/manage.py collectstatic --noinput
