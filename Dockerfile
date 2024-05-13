FROM python:3.11

ENV PYTHONPATH "${PYTHONPATH}:/app/src"

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install poetry

RUN pip3 install alembic

COPY pyproject.toml poetry.lock .

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

CMD ["python", "src/main.py"]
