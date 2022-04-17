FROM python:3.7-slim

RUN apt-get -y update
RUN apt-get install -y --fix-missing \
    libxml2 \
    gcc \
    vim \
    iputils-ping \
    telnet \
    procps \
    && apt-get clean && rm -rf /tmp/* /var/tmp/*

RUN pip install ray

CMD ["python", "script.py"]