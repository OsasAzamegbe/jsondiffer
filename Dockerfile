FROM ubuntu
WORKDIR /usr/src/jsondiffer
COPY . /usr/src/jsondiffer
RUN apt-get update && apt-get install -y \
    python3-pip \
    ruby-dev \
    && gem install fpm \
    && pip install -r requirements-dev.txt
