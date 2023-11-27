import struct
import ctypes
import json
import time

BROKER = '127.0.0.1'
PORT = 1883
TOPIC = "uav"
TOPIC_ALERT = "alert"

# coding=utf-8
import time
import socket
import random
 
# 组播组IP和端口
mcast_group_ip = '192.0.0.1'
mcast_group_port = 20000
 
def sender():
    # 建立发送socket，和正常UDP数据包没区别
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    local_ip = socket.gethostbyname(socket.gethostname())


    with open('20230814154308.bag', 'rb') as f:
        # 每十秒发送一遍消息
        while True:
            data = f.read(1024)
            send_sock.sendto(data, (mcast_group_ip, mcast_group_port))
            time.sleep(1)


if __name__ == "__main__":
    sender()

