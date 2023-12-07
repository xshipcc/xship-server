# !/bin/bash

#停止服务


pkill uav_sys
pkill uav_uav
pkill uav_api
pkill nanomq 
#启动服务

nohup nanomq start &
nohup ./uav_uav &
nohup ./uav_sys &
nohup ./uav_api &
