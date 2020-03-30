FROM python:2

USER root

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/

ADD timbot.py /

ADD database.py /

ADD config.yaml /

COPY images /images

CMD [ "python", "./timbot.py" ]
