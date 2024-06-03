# Use the official Python slim base image
FROM python:3.10-slim

# Install OS dependencies
RUN apt-get update && apt-get -y upgrade \
    && apt-get -y install --no-install-recommends curl build-essential \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install Poetry
ENV PATH="/root/.local/bin:$PATH"
RUN curl -sSL https://install.python-poetry.org | python3 - \
    && poetry --version

# Configure Poetry
ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_CACHE_DIR=/tmp/poetry_cache

# Set the working directory
WORKDIR /app

# Copy Poetry configuration and install dependencies
COPY pyproject.toml poetry.lock ./
RUN poetry install --only main && rm -rf $POETRY_CACHE_DIR

# Install dependencies
RUN poetry install --no-dev

# Copy the rest of the application code
COPY inscricoes /app/inscricoes

# Expose the port that the app runs on
EXPOSE 10101

# Define the command to run the app
CMD ["poetry", "run", "wave", "run", "inscricoes/app.py"]