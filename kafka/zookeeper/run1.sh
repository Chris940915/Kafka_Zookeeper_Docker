sudo docker run -i -t -d -p 2181:2181 -p 9092:9092 -p 8083:8083  --shm-size=8G \
	    --hostname kafka1 \
	    --network base_2 \
	    --ip 172.28.0.1 \
            -e DISPLAY=unix$DISPLAY \
            -e XAUTHORITY=/tmp/.docker.xauth \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
            -v /tmp/.docker.xauth:/tmp/.docker.xauth:rw \
            -v /home/keti-temp/Documents/dev/Seoultech/Database/twitter_event_detector/kafka/zookeeper/data1:/data:rw \
	    --name kafka_mongo_1 sostkr/base:4.0


