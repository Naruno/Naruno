FROM python:3.8-alpine

LABEL org.opencontainers.image.source https://github.com/Naruno/Naruno

RUN mkdir /app

RUN apk update

WORKDIR /app/

COPY Naruno Naruno

CMD [ "python3", "Naruno/naruno/cli/main.py"]
