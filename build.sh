# !/bin/bash


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

