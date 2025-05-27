FROM python:3.12-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip install --no-cache-dir --upgrade pip uv

COPY pyproject.toml uv.lock ./
RUN uv pip sync --no-cache --system uv.lock

COPY app ./app
COPY config.yaml ./config.yaml
COPY .env.example ./.env.example
COPY README.md ./README.md

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
