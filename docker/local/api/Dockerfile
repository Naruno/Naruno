FROM python:3.8-alpine

LABEL org.opencontainers.image.source https://github.com/Naruno/Naruno

RUN mkdir /app

RUN apk update

WORKDIR /app/

COPY Naruno Naruno

RUN pip install --no-cache-dir -r Naruno/requirements/api.txt

CMD [ "python3", "Naruno/naruno/api/main.py"]
