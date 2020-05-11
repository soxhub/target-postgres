FROM python:3.7.3-alpine
RUN apk add --update alpine-sdk bash postgresql-dev gcc python3-dev musl-dev netcat-openbsd

RUN mkdir -p /app
WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -e .

# install aws cli
RUN apk -Uuv add groff less python py-pip
RUN pip install awscli
RUN apk --purge -v del py-pip
RUN rm /var/cache/apk/*

CMD ["sh", "-c", "./run.sh"]
