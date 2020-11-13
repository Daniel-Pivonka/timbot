FROM python:2.7-slim

USER root

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/

COPY src /src
COPY images /images

CMD [ "python", "./src/timbot.py" ]
