# !/bin/bash

#停止服务


pkill uav_sys
pkill uav_uav
pkill uav_api
pkill MediaServer
pkill nanomq 
#启动服务

nohup ./MediaKit/MediaServer -d &
nohup nanomq start &
nohup ./uav_uav &
nohup ./uav_sys &
nohup ./uav_api &
