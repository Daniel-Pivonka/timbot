FROM go:2

USER root

COPY requirements.txt /tmp/
RUN pip install --requirement /tmp/requirements.txt
COPY . /tmp/

COPY src /src
COPY images /images

CMD [ "go", "./src/timbot.go" ]
