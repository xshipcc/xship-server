!/bin/bash

#停止服务

cd ~/SpireCV/ZLM/
./MediaServer -d &
cd ~/video/
ffmpeg -re -stream_loop -1 -i fd1.mp4 -c copy -an -vcodec libx264 -g 30 -crf 30 -strict -2 -s 600*400 -preset faster -profile:v main -x264-params bitrate=30000 -sc_threshold 1000000000 -f flv  rtmp://127.0.0.1/live/test