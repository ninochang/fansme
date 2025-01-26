# Dependency
FROM python:3.12.5-slim-bookworm AS dependencies
COPY --from=ghcr.io/astral-sh/uv:0.5.2 /uv /uvx /bin/
# ENV PATH="/usr/src/app/.venv/bin:$PATH"
WORKDIR /usr/src/app
COPY pyproject.toml uv.lock ./
# Install the application dependencies
RUN uv sync --frozen

# fansme
FROM python:3.12.5-slim-bookworm
ENV PATH="/usr/src/app/.venv/bin:$PATH"
WORKDIR /usr/src/app
COPY --from=dependencies /usr/src/app/.venv /usr/src/app/.venv
COPY . .

# Copy in the source code
EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
