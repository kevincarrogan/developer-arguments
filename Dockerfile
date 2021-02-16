FROM tiangolo/uvicorn-gunicorn-starlette:python3.8-alpine3.10

COPY . /app

ARG COMMIT_SHA
ENV RELEASE=${COMMIT_SHA}

RUN pip install -r /app/requirements-prod.txt
