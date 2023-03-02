FROM python:3.8-alpine

LABEL org.opencontainers.image.source https://github.com/Naruno/Naruno

RUN apk update
RUN apk --no-cache add git

RUN git clone https://github.com/Naruno/Naruno

CMD [ "python3", "Naruno/decentra_network/cli/main.py"]
