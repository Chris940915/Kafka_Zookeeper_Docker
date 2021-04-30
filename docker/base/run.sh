sudo docker run -i -t -d -p [HOST PORT]:[DOCKER PORT] --shm-size=8G \
            -e DISPLAY=unix$DISPLAY \
            -e XAUTHORITY=/tmp/.docker.xauth \
            -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
            -v /tmp/.docker.xauth:/tmp/.docker.xauth:rw \
            -v [HOST PATH]:[DOCKER PATH]:rw \
            --name [CONTAINER NAME] [DOCKER IMAGE]
