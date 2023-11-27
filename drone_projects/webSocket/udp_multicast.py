# udp_multicast.py
import struct
import socket
import threading
import time


class MulticastDataReceiver:
    def __init__(self, multicast_group, multicast_port, dest_addr, dest_port):
        self.multicast_group = multicast_group
        self.multicast_port = multicast_port

        self.dest_addr = dest_addr
        self.dest_port = dest_port

        self.sock = None
        self.thread_recv = None
        self.thread_send = None
        self.running = False

    def start(self):
        # # 创建UDP套接字
        # self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # # 允许端口复用
        # self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # # 绑定本机IP和组播端口
        # self.sock.bind(('', self.multicast_port))
        # # 设置UDP Socket的组播数据包的TTL（Time To Live）值
        # self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        # # 声明套接字为组播类型
        # self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        # # 加入多播组
        # # self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,socket.inet_aton(self.multicast_group) + socket.inet_aton('0.0.0.0'))
        # req = struct.pack("=4sl", socket.inet_aton(self.multicast_group), socket.INADDR_ANY)
        # self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, req)

        ## way 2
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        # 获取本地IP地址
        local_ip = socket.gethostbyname(socket.gethostname())
        # 监听端口，已测试过其实可以直接bind 0.0.0.0；但注意不要bind 127.0.0.1不然其他机器发的组播包就收不到了
        self.sock.bind(('', self.multicast_port))
        # 加入组播组
        # =表示本机字节顺序,标准大小,没有对齐.4s表示"四个字母的字符串"(四个字符串连接成一个字节
        # 串),l表示"签名长",在这种情况下是一个四字节的int.
        # 至于其余的代码,这是设置一个绑定到端口4242的多播udp监听mreq器.这个结构(C代码):
        mreq = struct.pack("=4sl", socket.inet_aton(self.multicast_group), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        
        self.running = True
        self.thread_recv = threading.Thread(target=self._receive_data)
        self.thread_send = threading.Thread(target=self._send_data)
        self.thread_recv.start()
        self.thread_send.start()

    def stop(self):
        self.running = False
        if self.thread_recv:
            self.thread_recv.join()
        if self.thread_send:
            self.thread_send.join()
        if self.sock:
            self.sock.close()

    # 接收数据
    def _receive_data(self):
        while self.running:
            data, address = self.sock.recvfrom(1024)
            print("----recv--- %s %s"%(data,address))
            #print(f"Received data from {address}: {data.decode()}")

    # 发送数据
    def _send_data(self):
        while self.running:
            data = "HLD"
            self.sock.sendto(data.encode(), (self.dest_addr, self.dest_port))
            # 休眠2秒
            time.sleep(2)

