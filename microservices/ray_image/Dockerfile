FROM python:2.7-slim

WORKDIR /usr/src/ray
COPY . /usr/src/ray

RUN apt-get -y update
RUN pip install ray

CMD ["python", "script.py"]