FROM python:3.8-alpine

LABEL org.opencontainers.image.source https://github.com/Decentra-Network/Decentra-Network

RUN apk update
RUN apk add git

RUN git clone https://github.com/Decentra-Network/Decentra-Network

CMD [ "python3", "Decentra-Network/src/cli.py"]
