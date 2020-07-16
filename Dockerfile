FROM python:3.8-alpine
RUN apk update && apk add postgresql-dev python3-dev gcc musl-dev libffi-dev openssl-dev

RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt

EXPOSE 5000

