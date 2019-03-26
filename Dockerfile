FROM ubuntu:18.04
LABEL maintainer="vasili.pascal@try.direct"

# no tty for container
ENV DEBIAN_FRONTEND noninteractive

# Install prerequisites
RUN apt-get update && apt-get install -y software-properties-common python-pip python-dev build-essential \
                                         libsdl1.2-dev libcurl4-gnutls-dev libgnutls28-dev python-dnspython libxslt1-dev \
                                         libxml2-dev swig portaudio19-dev libmysqlclient-dev python-m2crypto \
                                         libffi-dev dict libssl-dev supervisor libgcrypt20-dev
WORKDIR /app
COPY . /app
COPY supervisord.conf /etc/supervisord.conf

RUN pip install -r requirements.txt

ENTRYPOINT ["python"]
