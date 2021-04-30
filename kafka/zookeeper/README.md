# Setting

## 1. docker network setting

docker network create --gateway 172.28.5.254 --subnet 172.28.0.0/16 base_2

execute network.sh


## 2. build Dockerfile using build.sh
execute build.sh

## 4. make data1~3 directory
select 3 directory in host
and change host mount directory in run script

## 5. run script
execute run1.sh run2.sh run3.sh

## 6. execute zookeeper_start.sh in each container

## 7. execute kafka_start.sh in each container
