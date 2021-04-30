FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN rm -rf /var/lib/apt/lists/* &&\
    apt-get clean && \
    apt-get autoremove

RUN sed -i 's/security.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list && \
    sed -i 's/us.archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list && \
    sed -i 's/archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    wget \
    tar \
    ca-certificates \ 
    gcc \
    git \
    make \
    mercurial \
    cmake \
    unzip \
    pkg-config \
    python \
    python3 \
    python3-pip \
    python3-dev \
    libgtk2.0-dev \
    vim \
    rsync \
    python3-tk \
    curl \
    apt \
    multiarch-support \
    systemd-sysv \
    lsb-release \
    command-not-found \
    openssh-server \
    iptables \
    screen \
    && rm -rf /var/lib/apt/lists/*

RUN export PYTHONENCODING=utf-8 >> ~/.bashrc && \
    export PYTHONENCODING=utf-8

ARG user
ARG uid
ARG gid
ARG passwd
ARG display

ENV USERNAME ${user}

RUN echo "$USERNAME	ALL=NOPASSWD:	ALL" >> /etc/sudoers \
    && useradd -m $USERNAME \
    && echo "$USERNAME:$passwd" | chpasswd \
    && usermod --shell /bin/bash $USERNAME \
    && groupmod --gid ${gid} $USERNAME

USER ${user}
WORKDIR /home/${user}

RUN mkdir /home/${user}/Documents
