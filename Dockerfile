FROM python:2

USER root

RUN pip install slackclient numpy

COPY images /images
COPY lib /

CMD [ "python", "./timbot.py" ]
