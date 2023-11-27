# coding=utf-8
import time
import socket
import random
 
# 组播组IP和端口
mcast_group_ip = '239.0.0.1'
mcast_group_port = 23456
 
def sender():
    # 建立发送socket，和正常UDP数据包没区别
    send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    local_ip = socket.gethostbyname(socket.gethostname())
    # 每十秒发送一遍消息
    while True:
        t_int = random.randint(1, 20)
        message = f"{t_int} :this message send via mcast !"
        send_sock.sendto(message.encode(), (mcast_group_ip, mcast_group_port))
        print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: {local_ip}-> multicast {t_int} message send finish')
        time.sleep(2)
if __name__ == "__main__":
    sender()