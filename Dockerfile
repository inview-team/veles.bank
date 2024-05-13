FROM python:3.11

WORKDIR /app

RUN pip3 install --upgrade pip

RUN pip3 install poetry

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry config virtualenvs.create false && poetry install --no-dev

COPY . .

WORKDIR /app/src

CMD fastapi run src.main:app --port 30004
