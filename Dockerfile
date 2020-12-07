FROM python:3.8-alpine

RUN echo "http://dl-cdn.alpinelinux.org/alpine/edge/main" > /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories \
    && echo "http://dl-cdn.alpinelinux.org/alpine/v3.12/main" >> /etc/apk/repositories

RUN apk add \
    libstdc++ \
    chromium \
    harfbuzz \
    nss \
    freetype \
    ttf-freefont \
    font-noto-emoji \
    wqy-zenhei \
    py3-numpy \
    py3-pandas \
    && rm -rf /var/cache/* \
    && mkdir /var/cache/apk

RUN apk add chromium-chromedriver musl-dev linux-headers g++

WORKDIR /usr/src/app

ENV PYTHONPATH=/usr/lib/python3.8/site-packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY examples/ ./