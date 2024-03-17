FROM python:3.10-slim

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN \
    pip install poetry && \
    poetry install --no-root

# COPY ./app /code/app

# CMD ["poetry", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--reload"]
