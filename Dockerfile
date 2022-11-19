FROM python:3.11-alpine
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
RUN pip install -r requirements.txt

RUN crontab crontab


