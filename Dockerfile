FROM shroominic/python-uv:3.12

LABEL maintainer="Penn Labs"

# Copy project dependencies
COPY uv.lock /app/

# Copy project files
COPY . /app/

ENV DJANGO_SETTINGS_MODULE penncfa.settings.production
ENV SECRET_KEY 'temporary key just to build the docker image'

# Implicitly sync dependencies and collect static files
RUN uv run /app/manage.py collectstatic --noinput
