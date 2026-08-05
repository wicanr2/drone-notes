FROM ghcr.io/astral-sh/uv:python3.12-bookworm-slim

WORKDIR /app

COPY pyproject.toml ./
COPY src ./src

# 容器內建立 venv,不污染系統 Python。
RUN uv venv && uv pip install -e ".[mavsdk,dev]"
ENV PATH="/app/.venv/bin:$PATH"

COPY tests ./tests
COPY scripts ./scripts
COPY scenarios ./scenarios
COPY examples ./examples

EXPOSE 8000
CMD ["uvicorn", "mc.api:app", "--host", "0.0.0.0", "--port", "8000"]
