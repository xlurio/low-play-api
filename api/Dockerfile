FROM python:3.9.12-bullseye
LABEL Lucas Calegario

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY requirements.txt /requirements.txt
RUN python3 -m pip install --upgrade pip && \
    pip install -r requirements.txt

WORKDIR /api
COPY ./api /api
RUN python3 -m pip install -e .

RUN useradd -ms /bin/bash user
RUN chown -R user .
USER user
