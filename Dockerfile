FROM python:2

USER root

RUN pip install slackclient

ADD timbot.py /

COPY images /images

CMD [ "python", "./timbot.py" ]
