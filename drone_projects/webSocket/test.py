import socket
import struct

# 组播组的IP和端口
MCAST_GRP = '192.168.8.200'
MCAST_PORT = 14550

# 创建一个UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# 允许多个socket绑定到同一个端口号
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# 绑定到对应的地址和端口上
sock.bind(('', MCAST_PORT))

# 告诉操作系统将socket加入指定的组播组
# mreq = struct.pack("4sl", socket.inet_aton(MCAST_GRP), socket.INADDR_ANY)
# sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

# 设置超时时间，如果需要可以省略
sock.settimeout(5)

try:
    # 循环接收数据
    while True:
        try:
            # 接收数据
            data, addr = sock.recvfrom(1024)
            print(f"Received message: {data} from {addr}")

            # 如果需要发送数据回应
            message = "This is a response.".encode('utf-8')
            sock.sendto(message, addr)
        except socket.timeout:
            print('Timeout occurred, no data received.')
        except KeyboardInterrupt:
            print('Exited by user')
finally:
        # 关闭socket
    sock.close()