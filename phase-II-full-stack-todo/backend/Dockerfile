FROM python:3.13-slim

WORKDIR /app

# (Optional but common) system deps for building some Python wheels
RUN apt-get update \
  && apt-get install -y --no-install-recommends build-essential \
  && rm -rf /var/lib/apt/lists/*

# Install uv and sync dependencies from uv.lock
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv \
  && uv sync --frozen --no-dev

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
