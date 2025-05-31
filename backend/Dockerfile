FROM python:3

RUN python -m pip install --upgrade pip
WORKDIR /app

COPY ./requirements.txt $WORKDIR
RUN python -m pip install --no-cache-dir -r ./requirements.txt