`#### 项目前端是基于Ant Design Pro来创建的，后端是基于go-zero来创建的一个前后端分离的管理系统
# 1.项目介绍

AI计算 ： YOLO8 Python 引擎

ps aux | grep python3

226.0.0.80

MQ消息引擎:NANO MQ


#install mqtt 
$ git clone https://github.com/eclipse/paho.mqtt.c.git
$ cd paho.mqtt.c
$ git checkout v1.3.8

$ cmake -Bbuild -H. -DPAHO_ENABLE_TESTING=OFF -DPAHO_BUILD_STATIC=ON \
    -DPAHO_WITH_SSL=ON -DPAHO_HIGH_PERFORMANCE=ON
$ sudo cmake -DPAHO_BUILD_STATIC=TRUE -DPAHO_WITH_SSL=TRUE ..
$ sudo ldconfig



流媒体引擎：ZLMediaKit

安装Redis

git clone --depth 1 https://gitee.com/xia-chu/ZLMediaKit
cd ZLMediaKit
#千万不要忘记执行这句命令
git submodule update --init
# 安装gcc
sudo apt-get install build-essential
# 安装cmake
sudo apt-get install cmake
# 安装依赖库
#除了openssl,其他其实都可以不安装
sudo apt-get install libssl-dev -y
sudo apt-get install libsdl-dev -y
sudo apt-get install libavcodec-dev -y
sudo apt-get install libavutil-dev -y
sudo apt-get install ffmpeg -y
# 构建和编译项目
cd ZLMediaKit
mkdir build
cd build
cmake ..
# 如果编译release版本 使用 cmake .. -DCMAKE_BUILD_TYPE=Release
make -j4

运行：
cd ZLMediaKit/release/linux/Debug
#通过-h可以了解启动参数
./MediaServer -h
#以守护进程模式启动
./MediaServer -d &
./MediaServer -d default.pem -d

管理数据库：:Mysql,postgrsql
use mysql; 

alter user 'root'@'localhost' identified with mysql_native_password by '12345678';   

flush privileges;

服务器端：GO :web system 
download  ARM,AMD64  
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.14.3.linux-amd64.tar.gz

vi ~/.bashrc
export PATH=$PATH:/usr/local/go/bin

go env -w  GOPROXY=https://goproxy.io,direct

gst-launch-1.0 rtspsrc location='rtsp://web_camera_ip' ! rtph264depay ! h264parse ! fakesink

实时数据存储:rethinkdb
https://rethinkdb.com/docs/install/ubuntu/

python3 client.py 192.168.8.200 
# 推流
# h264推流

ffmpeg -re -i "/path/to/test.mp4" -vcodec h264 -acodec aac -f rtsp -rtsp_transport tcp rtsp://127.0.0.1/live/test
# h265推流
ffmpeg -re -i "/path/to/test.mp4" -vcodec h265 -acodec aac -f rtsp -rtsp_transport tcp rtsp://127.0.0.1/live/test

# Play
gst-launch-1.0 playbin uri=rtsp://127.0.0.1:5554/live/test

# 轮回推流

ffmpeg -re -stream_loop -1 -i drone.mp4 -c copy -f rtsp rtsp://127.0.0.1/live/test

ffmpeg -re -stream_loop -1 -i car2.mp4 -c copy -f flv rtmp://127.0.0.1/live/test


ffmpeg -re -stream_loop -1 -i 1.mp4 -c copy -an -vcodec libx264 -g 30 -crf 30 -strict -2 -s 600*400 -preset faster -profile:v main -x264-params bitrate=30000 -sc_threshold 1000000000 -f flv  rtmp://127.0.0.1/live/test



const char *jsonStr = "{\"name\":\"John\",\"age\":30,\"city\":\"New York\"}";

tcpdump -i eth0 tcp port 22

tcpdump -nX port 80 -r http.cap//16进制显示80端口的信息
tcpdump udp port 10000


ffmpeg -rtsp_transport tcp -r 25 -i rtsp://uer:gd123456@192.168.2.121:554/Streaming/Channels/101 -an -vcodec libx264 -g 30 -crf 30 -strict -2 -s 600*400 -preset faster -profile:v main -x264-params bitrate=300 -sc_threshold 1000000000 -f flv rtmp://192.168.35.75:1987/live/qmcy1111

ffmpeg -rtsp_transport tcp -i rtsp://admin:thinker13@192.168.0.240:554/streaming/channels/701 -acodec copy -vcodec  copy  video_test.mp4

ffmpeg -rtsp_transport tcp -i rtsp://192.168.8.160:554/live/track0 -an -vcodec libx264 -g 30 -crf 30 -strict -2 -s 600*400 -preset faster -profile:v main -x264-params bitrate=300 -sc_threshold 1000000000 -f flv rtmp://192.168.174.128:3519/live/ifmP0eWIg?sign=mBiEA6ZSRz


ffmpeg -rtsp_transport tcp -i rtsp://192.168.8.160:554/live/track0 -an -vcodec libx264 -g 30 -crf 30 -strict -2 -preset faster -profile:v main -x264-params bitrate=300 -sc_threshold 1000000000 -f flv rtmp://127.0.0.1/live/test

监控 http://127.0.0.1:8880/live/test.live.flv


# 数据备份
mysqldump -u root -p  --databases gozero > gozero.db


# 2.项目预览

**预览地址**http://127.0.0.1/ <span  style="color: red;"> 账号：admin 密码: 123456</span>

## 1.1用户 sys模块

安装启动模块
添加 gnome-terminal -- bash -c "/javodata/run.sh;exec bash"
gnome-terminal 	启动终端
-- 		运行环境
-c 		运行命令
; 		分割命令
exec bash	阻止窗口关闭

### 1.1.1新增用户


ps aux | grep python3



## 1.2角色



### 1.2.1分配权限



## 1.3菜单



## 1.4机构



## 1.5字典


## 1.6日志


## 1.7职位列表


# 2.AI计算部分
##############################Ubuntu20.04+CUDA11.6 #############################

sudo apt update && sudo apt install git cmake

cd ~ && git clone https://gitee.com/amovlab/SpireCV.git
cd ~/SpireCV/scripts/x86-cuda

# CUDA116+CUDNN841+TensorRT8406
chmod +x ubuntu2004-cuda-cudnn-11-6.sh && ./ubuntu2004-cuda-cudnn-11-6.sh
# 安装完成后需要重启

# GStreamer
chmod +x gst-install.sh && ./gst-install.sh

# FFmpeg
chmod +x ffmpeg425-install.sh && ./ffmpeg425-install.sh

# OpenCV4
chmod +x opencv470-install.sh && ./opencv470-install.sh

# Copy基础配置文件
cd ~/SpireCV && mkdir confs
cp params/a-params/* confs/
cp params/c-params/* confs/


# 桌面安装程序
cd ~/Desktop    ##进入当前用户桌面
vim pycharm.desktop   ##创建pycharm.desktop文件并进入编辑界面


[Desktop Entry]    (这行必须存在，笔者亲测把它注释掉后就会提示Broken Desktop File，即已损坏的桌面文件。）
Name=uav    (该快捷方式的名称）
Comment=uav shortcut    （对该文件的注释）
Exec=/javodata/run.sh   (执行文件的绝对路径，这里注意后缀.sh必须要写上，不然的话会报和之前一样的错误）
Type=Application   （类型，应用）
Terminal=false       （这个字段表示是否在执行时打开终端）
Icon=/javodata/icon.png     （指定应用图标文件）


sudo chmod +x ~/Desktop/xxx.desktop  #文件名

##############################intel CPU #############################

sudo apt update && sudo apt install git cmake

cd ~ && git clone https://gitee.com/amovlab/SpireCV.git
cd ~/SpireCV/scripts/x86-intel

# 1.LibVA 和 Media-Driver 的安装
chmod +x libva-install.sh && ./libva-install.sh

# 2.安装 OpenCL & VAAPI
chmod +x opencl-vaapi-install.sh && ./opencl-vaapi-install.sh

# 3.ffmpeg 
chmod +x ffmpeg-install.sh && ./ffmpeg-install.sh

# 4. ZLM
chmod +x zlm-server-install.sh && ./zlm-server-install.sh

# 5. OpenVINO 2022.3
chmod +x openvino-install.sh && ./openvino-install.sh

# 6. OpenCV4
chmod +x opencv470-install.sh && ./opencv470-install.sh

# Copy基础配置文件
cd ~/SpireCV && mkdir confs
cp params/a-params/* confs/
cp params/c-params/* confs/

echo "export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH" >> ~/.bashrc
source ~/.bashrc


# 2.1 如何报警，no tracker 方式。报警很多
              tracker 方式，跟踪一个对象 选一张图，保存报警，或者这个对象报警之后。再就不报警。靠人工去审查。
# 2.2 存录像，存带描边的录像。

# 2.3 AI 系统优化，支持大分辨率 ，窗口模式识别，大大提高识别率。

Drone_projects :管理部分c
启动drone_projects/drone_yolov8_deploy_show.py


剩余收尾工作总结：
1.无人机控制收发测试
2.无人机运行数据保存，存文件？
3.无人AI报警数据存储
4.无人机 摄像头和 载具配置后台保存
5.对接海康NVR人脸和车牌
6.无人机回放飞行数据
7.无人机飞行数据统计
8.无人机飞行数据可视化

AI：


回放：
拖拉显示


巡检历史，是否正常结束，中断结束。
报表：巡检记录通
每日巡检记录统计，


Redis：
总统计：
总完成率
总巡检时间
首页统计
系统统计：



隐藏：
告警类型
告警级别

新加硬件：
喊话
摇杆

后台：
监控参数
告警
统计表每日：统计。告警数量，告警类型，
总告告警数，分类告警数。
根据日期查询报表
根据时间段 查询 总报警数报表



AI：
1.人脸识别
2.车牌识别
3.轨迹识别

rtsp://admin:yd11223344@192.168.8.64:554/Streaming/Channels/101
rtsp://admin:yd11223344@192.168.8.65:554/Streaming/Channels/101