#! /bin/bash

# hostnmae 입력으로 받아서 숫자만 추출.
# 숫자 갑으로 4개 넣기. 
host_name=$(hostname -s)
myid=${host_name:5:1}
echo ${myid} >> /data/myid

sed -i '21d' /root/kafka/config/server.properties
sed -i '21 i\broker.id='${myid} /root/kafka/config/server.properties

#echo advertised.listeners=PLAINTEXT://kafka${myid}:9092 >> /root/kafka/config/server.properties
#echo advertised.host.name=kafka${myid} >> /root/kafka/config/server.properties
cp /etc/hosts2 /etc/hosts

# Start the Zookeeper first

/root/zookeeper/bin/zkServer.sh start
status=$?

if [ $status -ne 0 ]; then
  echo "Failed to start zookeeper: $status"
  exit $status
fi


