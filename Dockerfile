FROM python:3.10

WORKDIR /python-app

COPY . /python-app
RUN python3 -m pip install -r requirements.txt
