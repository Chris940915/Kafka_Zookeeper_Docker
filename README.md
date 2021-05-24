# MongoKafka


## 개요

본 프로젝트는 Database 팀 프로젝트로 진행하였습니다. SNS 이용자들은 자신의 일상을 SNS에 업로드하여 다른 사람들과 공유한다. SNS에 업로드된 일상 데이터에는 예상치 못한 사건, 행동 패턴들을 포함한다. 본 프로젝트에서는 SNS에 업로드된 데이터에서 예상치 못한 사건과 행동 패턴을 인공신경망 모델과 군집화 알고리즘을 활용하여 분석하는 Event Detection과 실시간 데이터를 취득하기 위하여 Kafka, zookeeper를 사용한 실시간 데이터 프레임워크를 제안한다. 제안한 Event Detection과 실시간 데이터 프레임워크를 검증하기 위하여 Twitter Streaming API를 활용하여 데이터를 취득하고 취득된 데이터를 활용하여 Event Detection의 성능을 검증한다. 이 프레임워크의 확장성 측면을 고려하여 Docker로 Kafka를 cluster로 구성하고 분석한다. 

## 위치 설명

#### kafka/cluster : kafka cluster를 Docker로 구성. 
#### cluster : cluster 를 analysis하는 코드. 

## Docker 사용법 

#### 1. docker network setting

docker network create --gateway 172.28.5.254 --subnet 172.28.0.0/16 base_2

execute network.sh

#### 2. build Dockerfile using build.sh
execute build.sh

#### 3. make data1~3 directory
select 3 directory in host
and change host mount directory in run script

#### 4. run script
execute run1.sh run2.sh run3.sh

#### 5. execute zookeeper_start.sh in each container

#### 6. execute kafka_start.sh in each container
