FROM ubuntu:16.04

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"

ENV TZ=Asia/Seoul

RUN apt-get update \
    && apt-get install -y \
    cron \
    build-essential \
    python3-pip \
    chromium-browser \
    tzdata \
    vim

COPY . /app

RUN pip3 install -U pip && pip install selenium slacker
RUN chmod -R 755 /app

RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

WORKDIR /app

ENTRYPOINT ["/app/start"]
