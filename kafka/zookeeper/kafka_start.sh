#! /bin/bash

# Start Kafka 

/root/kafka/bin/kafka-server-start.sh /root/kafka/config/server.properties
status =$?
if [ $status -ne 0 ]; then
  echo "Failed to start zookeeper: $status"
  exit $status
fi



