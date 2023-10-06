FROM python:3.11 as python-base
RUN mkdir fastapi_app
WORKDIR  /fastapi_app
COPY /pyproject.toml /fastapi_app
RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install
COPY . .
CMD ["gunicorn", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "src.api:app", "--bind", "0.0.0.0:8000"]
