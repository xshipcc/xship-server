# !/bin/bash

#安装go代理服务器
export GOPROXY=https://goproxy.cn

#AI mqtt 
git clone https://github.com/eclipse/paho.mqtt.c.git
cd paho.mqtt.c
cmake ..
sudo make install 
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

sudo apt-get install curl -y

sudo apt-get install nginx -y

curl -s https://assets.emqx.com/scripts/install-nanomq-deb.sh | sudo bash
sudo apt-get install nanomq -y


echo "system package installed....have fun ..."
