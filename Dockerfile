FROM python:3.10 AS BUILDER

# Configure Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .

RUN pip install -U pip &&  \
    pip install --no-cache-dir -r requirements.txt

FROM python:3.10-slim

# Configure Python
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Static files defaults
ENV STATIC_URL="/assets/"
ENV STATIC_ROOT="/var/django/.static"

# Media files defaults
ENV MEDIA_URL="/media/"
ENV MEDIA_ROOT="/var/django/.media"

RUN apt-get update && \
    apt-get dist-upgrade -y && \
    apt-get -y --no-install-recommends install \
    nginx \
    curl \
    nano \
    gettext \
    postgresql-client && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /etc/nginx/sites-enabled/default

WORKDIR /var/django

# Move template files for proxy
COPY .docker/templates /etc/nginx/templates
# Move venv
COPY --from=BUILDER /opt/venv /opt/venv
# Copy application
COPY . .

# Use venv from Backend
ENV PATH="/opt/venv/bin:$PATH"

ENTRYPOINT ./.docker/entrypoint.sh

EXPOSE 80
EXPOSE 8000
EXPOSE 5555
