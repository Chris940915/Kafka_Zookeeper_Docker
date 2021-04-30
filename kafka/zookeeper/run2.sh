sudo docker run -i -t -d -p 2182:2181 -p 9093:9092 -p 8084:8083  --shm-size=8G \
	    --hostname kafka2 \
	    --network base_2 \
	    --ip 172.28.0.2 \
            -e DISPLAY=unix$DISPLAY \
            -e XAUTHORITY=/tmp/.docker.xauth \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
            -v /tmp/.docker.xauth:/tmp/.docker.xauth:rw \
            -v /home/keti-temp/Documents/dev/Seoultech/Database/twitter_event_detector/kafka/zookeeper/data2:/data:rw \
	    --name kafka_mongo_2 sostkr/base:4.0


