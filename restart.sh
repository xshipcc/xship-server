!/bin/bash
#回到代码仓库
cd ~/Server/

pkill uav_sys
pkill uav_uav
pkill uav_api
pkill MediaServer
pkill nanomq 



#构建服务
cd api
go build
mv api ../uav_api
cd ..

#系统服务
cd rpc/sys
go build
mv sys ../../uav_sys
cd ../../

#用户UAV
cd rpc/uav
go build
mv uav ../../uav_uav
cd ../../

#复制程序
cp uav_* /javodata/ -rf
cp drone_projects /javodata/ -rf
#启动服务

cd /javodata/
./MediaKit/MediaServer -d &
nanomq start &
nohup ./uav_sys &
nohup ./uav_api &
./uav_uav
