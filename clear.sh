#!/usr/bin/env bash

sudo mn -c

docker stop $(docker ps -aq)

sudo ip link delete gnb-s1
sudo ip link delete s1-s2
sudo ip link delete core-s2
sudo ip link delete webui-s2