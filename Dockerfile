FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8-slim
COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/
COPY ./app/ /app/app/