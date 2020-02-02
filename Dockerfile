FROM tiangolo/meinheld-gunicorn-flask:python3.7

COPY . /app

RUN pip install -r /app/requirements.txt
