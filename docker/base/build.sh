sudo docker build --build-arg user="ubuntu" --build-arg passwd="[PASSWD]" --build-arg uid=$(id -u) --build-arg gid=$(id -g) --build-arg display=$DISPLAY --tag [DOCKER IMAGE NAME] .
