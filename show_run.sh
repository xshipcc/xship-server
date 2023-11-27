# !/bin/bash

#停止服务


pkill uav_sys
pkill uav_uav
pkill uav_api
pkill MediaServer
pkill nanomq 
#启动服务

./MediaKit/MediaServer -d &
nanomq start &
./uav_uav &
./uav_sys &
./uav_api &
