sudo docker run -i -t -d -p 2183:2181 -p 9094:9092 -p 8085:8083  --shm-size=8G \
	    --hostname kafka3 \
	    --network base_2 \
	    --ip 172.28.0.3 \
            -e DISPLAY=unix$DISPLAY \
            -e XAUTHORITY=/tmp/.docker.xauth \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
            -v /tmp/.docker.xauth:/tmp/.docker.xauth:rw \
            -v /home/keti-temp/Documents/dev/Seoultech/Database/twitter_event_detector/kafka/zookeeper/data3:/data:rw \
	    --name kafka_mongo_3 sostkr/base:4.0


