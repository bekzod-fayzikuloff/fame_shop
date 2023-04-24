FROM python:3.11-bullseye

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# System deps:
RUN apt-get update \
  && apt-get install --no-install-recommends -y \
    bash \
  # Cleaning cache: \
  && /usr/local/bin/python -m pip install --upgrade pip \
  && pip3 install poetry && echo "Poetry installed successfully"

# set work directory
WORKDIR /app

ENV PATH="${PATH}:/root/.poetry/bin"
COPY pyproject.toml poetry.lock /app/

# Install dependencies
RUN poetry install --no-root

COPY . /app/
