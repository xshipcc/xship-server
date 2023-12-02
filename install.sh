# !/bin/bash

#安装go代理服务器
export GOPROXY=https://goproxy.cn
#安装视频服务
git clone --depth 1 https://gitee.com/xia-chu/ZLMediaKit
cd ZLMediaKit
#千万不要忘记执行这句命令
git submodule update --init
# 安装gcc
sudo apt-get install build-essential -y
# 安装cmake
sudo apt-get install cmake  -y
# 安装依赖库
#除了openssl,其他其实都可以不安装
sudo apt-get install libssl-dev -y
sudo apt-get install libsdl-dev -y
sudo apt-get install libavcodec-dev -y
sudo apt-get install libavutil-dev -y
sudo apt-get install ffmpeg -y
#安装人脸识别库
sudo apt-get install cmake libopenblas-dev liblapack-dev libjpeg-dev -y
sudo apt install nvidia-cuda-dev -y
# 构建和编译项目
cd ZLMediaKit
mkdir build
cd build
cmake ..
# 如果编译release版本 使用 cmake .. -DCMAKE_BUILD_TYPE=Release
make -j4
cd ..
cd ..
cp -f zlmedia.ini ZLMediaKit/release/linux/Debug/ 
cp -rf ZLMediaKit/release/linux/Debug /javodata/MediaKit
cp run.sh /javodata/
cp run_show.sh /javodata/

#AI mqtt 
git clone https://github.com/eclipse/paho.mqtt.c.git
cd paho.mqtt.c
cmake ..
sudo make install 
cd ..


#install SpritCV AI system 
git clone https://github.com/eclipse/paho.mqtt.c.git
cd paho.mqtt.c
cmake ..
sudo make install 
cd ..

# GStreamer
wget https://download.amovlab.com/model/scripts/common/gst-install-orin.sh
chmod +x gst-install-orin.sh
./gst-install-orin.sh

# OpenCV4
wget https://download.amovlab.com/model/scripts/jetson/opencv470-jetpack511-install.sh
chmod +x opencv470-jetpack511-install.sh
./opencv470-jetpack511-install.sh

git clone https://e.coding.net/magixmin/UAV/SpireCV.git
cd SpireCV
./build_on_jetson.sh
#downlaod other model 
chmod +x models-downloading.sh
./models-downloading.sh
#comver to jeston NX
chmod +x models-converting.sh
./models-converting.sh

cd ..



pip3 install -r drone_projects/requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple 

# 安装视频NVR服务
#git clone https://github.com/panjjo/gosip.git
#cd gosip
#make
#cd ..
# 安装Python
pip3 install ffmpeg



cd ..
sudo apt-get install redis-server  -y
sudo apt-get install mysql-server  -y



#opencv
apt-get install ffmpeg libsm6 libxext6 -y
apt-get install libgl1 -y

apt-get install curl -y

apt-get install nginx -y

curl -s https://assets.emqx.com/scripts/install-nanomq-deb.sh | sudo bash
sudo apt-get install nanomq -y

#add server start 
sudo cp uav.service /etc/systemd/system/uav.service
sudo systemctl start uav.service
sudo systemctl enable uav.service

echo "system package installed....have fun ..."
