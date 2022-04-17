FROM python:3.7-slim

WORKDIR /usr/src/ray
COPY . /usr/src/ray

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    libxml2 \
    gcc \
    vim \
    iputils-ping \
    telnet \
    procps \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*
RUN pip install psutil

RUN pip install -U "ray[default]" google-api-python-client

CMD ["ray up -y config.yaml && ray submit config.yaml script.py"]