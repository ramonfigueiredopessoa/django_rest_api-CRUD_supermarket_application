FROM python:3.7-alpine

# Setting PYTHONUNBUFFERED to a non-empty value different from 0 ensures that the python output i.e. the stdout and
# stderr streams are sent straight to terminal (e.g. your container log) without being first buffered and that you can
# see the output of your application (e.g. django logs) in real time.
ENV PYTHONUNBUFFERED 1

RUN mkdir /code

WORKDIR /code

COPY . /code/

RUN pip install -r requirements.txt
