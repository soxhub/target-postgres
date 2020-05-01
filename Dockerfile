FROM python:3.7.3-alpine
RUN apk add --update alpine-sdk bash postgresql-dev gcc python3-dev musl-dev netcat-openbsd

RUN mkdir -p /app
WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -e .

CMD ["sh", "-c", "./run.sh"]
