FROM tiangolo/uvicorn-gunicorn-starlette:python3.7-alpine3.8

COPY . /app

RUN pip install -r /app/requirements-prod.txt
