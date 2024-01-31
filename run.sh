#!/bin/bash
#停止服务

cd /javodata/
pkill uav_sys
pkill uav_uav
pkill uav_api
pkill nanomq 
pkill python3
pkill python3
pkill python3
pkill python3
#启动服务

nohup nanomq start &
sleep 5
nohup ./uav_sys &
nohup ./uav_api &
./uav_uav
