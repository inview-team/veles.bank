FROM python:3.11-alpine

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

RUN pip3 install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock .

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

CMD ["python", "src/main.py"]