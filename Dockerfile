FROM python:3.10

WORKDIR /app

# Install Poetry
RUN pip install --no-cache-dir poetry

# Copy pyproject.toml and poetry.lock files
COPY pyproject.toml poetry.lock* ./

# Regenerate the poetry.lock file to reflect changes in pyproject.toml
RUN poetry lock --no-update

# Install dependencies
RUN poetry install --only main --no-root

# Copy the application code
COPY . .

# Ensure Python finds the 'src' module
ENV PYTHONPATH=/app/src

# Set the entry point for the container
CMD ["poetry", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8019", "--reload"]