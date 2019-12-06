FROM python:2

USER root

RUN pip install slackclient numpy

ADD timbot.py /

COPY images /images

CMD [ "python", "./timbot.py" ]
