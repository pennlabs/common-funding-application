FROM ghcr.io/astral-sh/uv:0.6.2-python3.12-bookworm

LABEL maintainer="Penn Labs"

# Copy project files
COPY . /app/
COPY ./scripts/mime.types /etc/mime.types
COPY ./scripts/django-run /usr/local/bin/

WORKDIR /app
RUN uv sync --frozen

ENV DJANGO_SETTINGS_MODULE penncfa.settings.production
ENV SECRET_KEY 'temporary key just to build the docker image'
ENV PATH="/app/.venv/bin:$PATH"

# Collect static files
RUN uv run /app/manage.py collectstatic --noinput
CMD ["/usr/local/bin/django-run"]