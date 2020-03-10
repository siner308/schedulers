FROM ubuntu:16.04

ENV LC_ALL="C.UTF-8"
ENV LANG="C.UTF-8"

ENV TZ=Asia/Seoul

COPY ./google-chrome-stable_current_amd64.deb /google-chrome-stable_current_amd64.deb

RUN apt-get update && apt-get autoremove && apt-get autoclean \
    && apt-get install -y \
        vim \
        cron \
        tzdata \
        python3-pip \
        build-essential \
        libxss1 \
        libgconf2-4 \
        libappindicator1 \
        libindicator7 \
        fonts-liberation \
        libasound2 \
        libnspr4 \
        libnss3 \
        libx11-xcb1 \
        wget \
        xdg-utils \
        libappindicator3-1 \
        libatk-bridge2.0-0 \
        libatspi2.0-0 \
        libgtk-3-0 \
    && dpkg -i /google-chrome-stable_current_amd64.deb \
    && rm -rf /var/lib/apt/lists/* \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

COPY . /app

RUN pip3 install -U pip && pip install selenium slacker
RUN chmod -R 755 /app

WORKDIR /app

ENTRYPOINT ["/app/start"]
