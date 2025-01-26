FROM python:3.11-slim

WORKDIR /app

# Install Poetry
RUN pip install poetry

# Copy dependency files
COPY pyproject.toml poetry.lock ./

# Configure poetry to not create virtual environment in container
RUN poetry config virtualenvs.create false

# Install dependencies
RUN poetry install --no-dev

# Copy application code
COPY . .

# Run the application
CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"] 