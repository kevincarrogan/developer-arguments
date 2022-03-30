FROM tiangolo/uvicorn-gunicorn-starlette:python3.9-alpine3.14

COPY . /app

ARG COMMIT_SHA
ENV RELEASE=${COMMIT_SHA}

RUN pip install -r /app/requirements-prod.txt
