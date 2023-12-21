# coding=utf-8
import struct
import time
import socket
 
# 组播组IP和端口
MCAST_GRP = '192.168.8.50'
MCAST_PORT = 10001
 
 
def receiver():
    # 建立接收socket，和正常UDP数据包没区别
    # sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    # # 获取本地IP地址
    # local_ip = socket.gethostbyname(socket.gethostname())
    # # 监听端口，已测试过其实可以直接bind 0.0.0.0；但注意不要bind 127.0.0.1不然其他机器发的组播包就收不到了
    # sock.bind(('', mcast_group_port))
    # # 加入组播组
    # # =表示本机字节顺序,标准大小,没有对齐.4s表示"四个字母的字符串"(四个字符串连接成一个字节
    # # 串),l表示"签名长",在这种情况下是一个四字节的int.
    # # 至于其余的代码,这是设置一个绑定到端口4242的多播udp监听mreq器.这个结构(C代码):
    # mreq = struct.pack("=4sl", socket.inet_aton(mcast_group_ip), socket.INADDR_ANY)
    # sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)
 
    # # 允许端口复用，看到很多教程都有没想清楚意义是什么，我这里直接注释掉
    # sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 创建一个UDP socket
        
    # 创建一个UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

    # 允许多个socket绑定到同一个端口号
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    # 绑定到对应的地址和端口上
    sock.bind(('', MCAST_PORT))

    # 告诉操作系统将socket加入指定的组播组
    mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
    sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

    # 设置超时时间，如果需要可以省略
    sock.settimeout(5)

    # 设置非阻塞，看到很多教程都有也没想清楚有什么用，我这里直接注释掉
    # sock.setblocking(0)
    while True:
        try:
            message, addr = sock.recvfrom(1024)
            print(f'{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}: Receive data from {addr}: {message.decode()}')
            #print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
 
        except:
            print("while receive message error occur")
 
 
if __name__ == "__main__":
    receiver()