# 发送Hex数据：
# ```python
# 可以自动计算CRC的命令

import socket
import binascii


def crc16_direct(bytestr):
    '''
    crc16直接计算法
    :param bytestr: bytes字符串
    :return: int16类型
    '''
    crc = 0
    if len(bytestr) == 0:
        return 0
    for i in range(len(bytestr)):
        R = bytestr[i]
        for j in range(8):
            if R > 127:
                k = 1
            else:
                k = 0

            R = (R << 1) & 0xff
            if crc > 0x7fff:
                m = 1
            else:
                m = 0

            if k + m == 1:
                k = 1
            else:
                k = 0

            crc = (crc << 1) & 0xffff
            if k == 1:
                crc ^= 0x1021  # 多项式为 0x1021
    return crc


def main():
    # 创建UDP套接字
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # 目标地址和端口
    target_addr = ('192.168.10.188', 37260)
    # 发送的Hex数据

    # zoom 放大
    # hex_data = b'\x55\x66\x01\x01\x00\x00\x00\x05\x01\x8d\x64'
    # zoom 缩小
    # hex_data = b'\x55\x66\x01\x01\x00\x00\x00\x05\xff\x5c\x6a'

    # zoom 放大 no crc
    # hex_data = b'\x55\x66\x01\x01\x00\x00\x00\x05\x01'
    # zoom 缩小 no crc
    # hex_data = b'\x55\x66\x01\x01\x00\x00\x00\x05\xff'

    # 区别
    # 0x表示整型数值（0x42 -66为字母B的ASCII）
    # \x表示字符(0x42-B)

    # Hex()函数返回字符串而不是int hex?的处理方法
    # 不知道为什么Hex函数返回的字符串类似于'0x41'而不是0x41

    # protocol
    '''
    STX:2byte
        0x5566
    CTL:1byte
        0,need ack
        1,ack pack
    DataL: 2byte,
            0x1
            0x0
    SEQ：2byte
        0x00
        0x00
    CMD:1byte,
    DATA:DataL,
    CRC16:2byte,
    '''
    cmd1 = b'\x55\x66\x01\x01\x00\x00\x00'
    cmd2 = b'\x05\x01'  # 变大
    cmd3 = b'\x05\xff'  # 变小

    # 控制yaw  roll
    cmd4 = b'\x55\x66\x01\x04\x00\x00\x00'  #
    # cmd5 = b'\x0E\x00\x00\xab\xfe'   #
    cmd5 = b'\x0E\x00\x00\x00\xf0'  #

    # 组合命令,固定的几组命令
    cmd = cmd4 + cmd5

    print(cmd.hex())
    crc16 = crc16_direct(cmd)  # 直接计算法
    print("直接及算法：", crc16, hex(crc16), hex(crc16 & 0xff), hex(crc16 >> 8 & 0xff))
    print("直接及算法：", crc16, hex(crc16), hex(crc16 & 0xff)[2:].zfill(2), hex(crc16 >> 8 & 0xff)[2:].zfill(2))

    crch = "".join(hex(crc16 & 0xff)[2:].zfill(2))
    crcl = "".join(hex(crc16 >> 8 & 0xff)[2:].zfill(2))
    # print(crch)
    # print(crcl)

    mycmd = cmd.hex() + crch + crcl
    # print(cmd.hex()+crch+crcl)

    hex_data = binascii.a2b_hex(mycmd)
    sock.sendto(hex_data, target_addr)

    # 关闭套接字
    sock.close()


if __name__ == '__main__':
    main()
