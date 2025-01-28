ARG PYTHON_VERSION="3.12.5"
ARG UV_VERSION="0.5.2"

# UV
FROM ghcr.io/astral-sh/uv:${UV_VERSION} AS uv


# Dependency
FROM python:${PYTHON_VERSION}-slim-bookworm AS dependencies
COPY --from=uv /uv /uvx /bin/
WORKDIR /usr/src/app
COPY pyproject.toml uv.lock ./
RUN uv sync --frozen


# Fansme
FROM python:${PYTHON_VERSION}-slim-bookworm
ENV PATH="/usr/src/app/.venv/bin:$PATH"
WORKDIR /usr/src/app
COPY --from=dependencies /usr/src/app/.venv /usr/src/app/.venv
COPY . .

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
