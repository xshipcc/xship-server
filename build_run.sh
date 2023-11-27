# !/bin/bash

#停止服务
# pkill uav_oms
# pkill uav_pms
# pkill uav_sms
# pkill uav_cms
pkill uav_sys
pkill uav_uav
# pkill uav_ums
pkill uav_api
pkill MediaServer
pkill nanomq 

#删除容器

# rm uav_oms
# rm uav_pms
# rm uav_sms
# rm uav_cms
rm uav_sys
rm uav_uav
rm uav_api


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


# #用户系统
# cd rpc/ums
# go build
# mv ums ../../uav_ums
# cd ../../



# #用户系统
# cd rpc/cms
# go build
# mv cms ../../uav_cms
# cd ../../


# #sms
# cd rpc/sms
# go build
# mv sms ../../uav_sms
# cd ../../

# #pms
# cd rpc/pms
# go build
# mv pms ../../uav_pms
# cd ../../

# #oms
# cd rpc/oms
# go build
# mv oms ../../uav_oms
# cd ../../



#启动服务
./MediaKit/MediaServer -d &
nanomq start &
./uav_uav &
./uav_sys &
./uav_api &