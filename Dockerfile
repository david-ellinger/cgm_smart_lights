# syntax=docker/dockerfile:1
FROM python:3.11-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip install --upgrade pip
RUN pip3 install -r requirements.txt
COPY . .
ENV FLASK_APP=app
EXPOSE 3000
CMD ["python","app/app.py"]
