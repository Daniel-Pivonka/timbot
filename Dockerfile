FROM python:2

USER root

RUN pip install slackclient

ADD timbot.py /

CMD [ "python", "./timbot.py" ]
