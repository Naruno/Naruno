FROM python:3.8-alpine

RUN apk update
RUN apk add git

RUN git clone https://github.com/Decentra-Network/Decentra-Network

RUN pip install -r Decentra-Network/requirements/api.txt

CMD [ "python3", "Decentra-Network/src/api.py"]
