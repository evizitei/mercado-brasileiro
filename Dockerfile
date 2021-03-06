FROM python:3
ENV PYTHONUNBUFFERED=1
WORKDIR /app
# Install Postgres Client
RUN apt-get update && apt-get install -y postgresql
# Install Mongo Client
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add -
RUN echo "deb http://repo.mongodb.org/apt/debian buster/mongodb-org/4.4 main" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list
RUN apt-get update && apt-get install -y mongodb-org
# Install python dependencies
COPY requirements.txt /app/
RUN pip install -r requirements.txt
COPY . /app/