FROM ubuntu:18.04

ENV DEBIAN_FRONTEND=noninteractive

RUN rm -rf /var/lib/apt/lists/* &&\
    apt-get clean && \
    apt-get autoremove

RUN sed -i 's/security.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list && \
    sed -i 's/us.archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list && \
    sed -i 's/archive.ubuntu.com/ftp.daum.net/g' /etc/apt/sources.list

RUN apt-get update && \
    apt-get install -y --no-install-recommends apt-utils\
    software-properties-common && \
    add-apt-repository -y ppa:openjdk-r/ppa && \
    apt-get update && \
    apt-get install -y --no-install-recommends \
    software-properties-common \
    openjdk-8-jdk \
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

#ARG myid

RUN wget -P /root/ http://apache.mirror.cdnetworks.com/zookeeper/zookeeper-3.4.14/zookeeper-3.4.14.tar.gz && \
    wget -P /root/ http://apache.mirror.cdnetworks.com/kafka/2.2.2/kafka_2.12-2.2.2.tgz && \
    tar -zxvf /root/zookeeper-3.4.14.tar.gz -C /root && \
    tar -zxvf /root/kafka_2.12-2.2.2.tgz -C /root && \
    ln -s /root/zookeeper-3.4.14 /root/zookeeper && \
    ln -s /root/kafka_2.12-2.2.2 /root/kafka && \  
    mkdir /data /root/data1 /root/data2 && \
    # zookeeper setting start
    cp /root/zookeeper/conf/zoo_sample.cfg /root/zookeeper/conf/zoo.cfg && \
    echo server.1=kafka1:2888:3888 >> /root/zookeeper/conf/zoo.cfg && \
    echo server.2=kafka2:2888:3888 >> /root/zookeeper/conf/zoo.cfg && \
    echo server.3=kafka3:2888:3888 >> /root/zookeeper/conf/zoo.cfg && \    
    sed -i 's/tmp\/zookeeper/data/g' /root/zookeeper/conf/zoo.cfg && \
    # kafka setting start
    sed -i '60d' /root/kafka/config/server.properties && \ 
    sed -i '60 i\log.dirs=\/root\/data1, \/root\/data2' /root/kafka/config/server.properties && \
    #sed 's/broker.id=0/broker.id=${myid}' kafka/config/server.properties    
    # listner open 
    sed -i '31d' /root/kafka/config/server.properties && \    
    sed -i '31 i\listeners=PLAINTEXT:\/\/:9092' /root/kafka/config/server.properties && \  
    # zookeeper connect
    sed -i '123d' /root/kafka/config/server.properties && \
    sed -i '123 i\zookeeper.connect=kafka1:2181,kafka2:2181,kafka3:2181/twitter' /root/kafka/config/server.properties && \
    #echo advertised.listeners=PLAINTEXT://kafka${myid}:9092 >> /root/kafka/config/server.properties && \
    #echo advertised.host.name=kafka${myid} >> /root/kafka/config/server.properties && \
    echo \ >> /root/kafka/config/server.properties && \
    #echo advertised.host.name=9092 >> /root/kafka/config/server.properties && \   
    # /ect/hosts 파일에 DNS 등록. 
    cp /etc/hosts /etc/hosts2 && \
    sed -i '7d' /etc/hosts2 && \
    echo 172.28.0.1      kafka1 >> /etc/hosts2 && \
    echo 172.28.0.2      kafka2 >> /etc/hosts2 && \
    echo 172.28.0.3      kafka3 >> /etc/hosts2 && \
    echo 172.28.0.4      mongodb >> /etc/hosts2
   
# mongodb kafka connector install and configuration
RUN wget -P /root/ https://search.maven.org/remotecontent?filepath=org/mongodb/kafka/mongo-kafka-connect/1.1.0/mongo-kafka-connect-1.1.0.jar && \ 
    mkdir -p /root/kafka/plugins/kafka-connect-mongo && \
    mv /root/remotecontent\?filepath\=org%2Fmongodb%2Fkafka%2Fmongo-kafka-connect%2F1.1.0%2Fmongo-kafka-connect-1.1.0.jar /root/mongo-kafka-connect.jar && \ 
    cp /root/mongo-kafka-connect.jar /root/kafka/plugins/ && \
    cp /root/mongo-kafka-connect.jar /root/kafka/plugins/kafka-connect-mongo/ && \
    # worker configuration 
    echo bootstrap.servers=kafka1:9092,kafka2:9092,kafka3:9092 >> /root/kafka/config/connect.properties && \
    # path to directory containing the connector jar and dependencies
    echo plugin.path=/root/kafka/plugins >> /root/kafka/config/connect.properties && \
 
    echo key.converter=org.apache.kafka.connect.storage.StringConverter >> /root/kafka/config/connect.properties && \
    echo value.converter=org.apache.kafka.connect.storage.StringConverter >> /root/kafka/config/connect.properties && \
    echo internal.key.converter=org.apache.kafka.connect.json.JsonConverter >> /root/kafka/config/connect.properties && \
    echo internal.value.converter=org.apache.kafka.connect.json.JsonConverter >> /root/kafka/config/connect.properties && \  
    echo internal.key.converter.schemas.enable=false >> /root/kafka/config/connect.properties && \
    echo internal.value.converter.schemas.enable=false >> /root/kafka/config/connect.properties && \
    echo offset.storage.file.filename=/tmp/connect.offsets >> /root/kafka/config/connect.properties && \
    echo offset.storage.topic=test >> /root/kafka/config/connect.properties && \
    echo rest.host.name=connect >> /root/kafka/config/connect.properties && \
    echo rest.port=8083 >> /root/kafka/config/connect.properties && \
    echo group.id=test >> /root/kafka/config/connect.properties && \
    echo config.storage.topic=test >> /root/kafka/config/connect.properties && \ 
    echo config.storage.replication.factor=1 >> /root/kafka/config/connect.properties && \
    echo status.storage.topic=test >> /root/kafka/config/connect.properties && \
    # mongo sink configuration 
    echo name=mongo-sink >> /root/kafka/config/mongo-sink.properties && \
    echo tasks.max=1 >> /root/kafka/config/mongo-sink.properties && \
    echo topics=test >> /root/kafka/config/mongo-sink.properties && \
    echo connector.class=com.mongodb.kafka.connect.MongoSourceConnector >> /root/kafka/config/mongo-sink.properties && \    
    echo connection.uri=mongodb://mongodb:27017 >> /root/kafka/config/mongo-sink.properties && \
    echo databse=test >> /root/kafka/config/mongo-sink.properties && \
    echo collection=test >> /root/kafka/config/mongo-sink.properties 


RUN export PYTHONENCODING=utf-8 >> ~/.bashrc && \
    export PYTHONENCODING=utf-8

ARG user
ARG uid
ARG gid
ARG passwd
ARG display

WORKDIR /root

RUN mkdir /root/Documents

VOLUME ["/home/bigbase-2/Documents/twitter/kafka/zookeeper"]

COPY zookeeper_start.sh /root/Documents/zookeeper_start.sh
COPY kafka_start.sh /root/Documents/kafka_start.sh

#RUN bash /root/Documents/wrapper_script.sh

# CMD ["bash /root/Documents/wrapper_script.sh"]

#CMD ["zookeeper/bin/zkServer.sh start"] && \
#    ["kafka/bin/kafka-server-start.sh kafka/config/server.properties"]
