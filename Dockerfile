FROM tiangolo/uvicorn-gunicorn-starlette:python3.7-alpine3.8

COPY . /app

ARG COMMIT_SHA
ENV RELEASE=${COMMIT_SHA}

RUN pip install -r /app/requirements-prod.txt
