docker build --build-arg user="ubuntu" --build-arg passwd="ubuntu" --build-arg uid=$(id -u) --build-arg gid=$(id -g) --build-arg display=$DISPLAY --tag sostkr/base:4.0 .
