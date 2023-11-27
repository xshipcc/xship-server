# 项目介绍
无人机项目,无人机搭载nvidia jetson边缘计算板子,进行实时识别。
jetson上电,程序自动启动拉取rtsp或者usb获取视频流,每秒获取3张图片进行算法分析,算法分析之前每3秒保存一张图片,
每5秒保存一张识别后图片,同时识别后的图片实时添加gps信息(需要gps硬件模块);最终保留完整的识别视频。


### 功能简介

1. 程序开机启动
2. 从RTSP流或者USB摄像头获取视频流,进行算法识别。识别前每3秒保存一张图片,每5秒保存一张识别后图片
3. 识别后的图片添加gps信息,gps信息从北斗+gps设备获取
4. 保存识别后的视频流为`.avi`格式,需要经过转换成`.mp4`格式才能播放,参考`start_cover_video.sh`
5. 网页端实时查看识别后的视频流，视频延迟在1秒内
6. 网页端实时查看保存好的识别结果图片

cd UAVServer
git pull
cd drone

history | grep 192
python client.py 1232

nanomq start

### 代码结构
~~~
├── config
│   ├── nginx.conf  --nginx配置文件(暂时不用)
│   └── rc-local.service  --(jetson开机自启动服务)
├── drone_yolov8_deploy_noshow.py  --不弹窗显示
├── drone_yolov8_deploy_show.py  --弹窗显示
├── file  --文件目录
│   ├── detection  --检测结果图目录
│   │   ├── detection_{110}_{2023-06-29_20:39:22}_addgps.jpg  --检测到目标后增加gps信息的图片
│   │   └── detection_{110}_{2023-06-29_20:39:22}.jpg  --检测到目标后的图片
│   ├── gps  --gps测试目录
│   │   ├── 001_addgps.jpg
│   │   ├── 001.jpg
│   │   └── 002.jpg
│   └── origin  --原图目录
│       └── orgin_{150}_{2023-06-29_20:39:23}.jpg  --原图
├── model
│   ├── yolov8l_drone.pt  --yolov8模型文件
│   └── yolov8n.pt
├── README.md  --readme
├── requirements.txt  --依赖包文件
├── start_cover_video.sh  --视频转换脚本
├── start_noshow.sh  --后台启动脚本
├── start_show.sh  --后台启动脚本
├── temp.jpg
├── templates  --flask模板文件
│   ├── file.html
│   └── index.html
└── utils  --工具类目录
    ├── gps_utils.py
    ├── image_gps.py
    └── udp_utils.py
~~~

### 如何启动
开机自启动

# 开发者模式
### 1. 安装依赖环境
~~~
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
~~~
### 2. 启动程序
~~~
python drone_yolov8_deploy_show.py
~~~
或者
~~~
sh start_show.sh
~~~

# 其他
欢迎交流