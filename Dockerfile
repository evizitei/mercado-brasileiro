FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
RUN apt-get update && apt-get install -y postgresql
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/