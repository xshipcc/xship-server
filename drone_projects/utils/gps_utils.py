# coding:utf-8

import serial
import pynmea2
import binascii

"""
实时获取gps信息工具类
"""


def get_lat_lng():
    lat = 25
    lng = 144
    alt = 140
    return lat, lng, alt


# NMEA0183数据转换成度分秒格式
def nmea0183_to_dms(nmea):
    # 将NMEA0183格式的经纬度字符串转换为度分秒格式
    # 例如：输入为"4124.8963,N"，输出为"41°24'53.78"N"
    degrees = nmea[:2]
    minutes = nmea[2:]
    decimal_degrees = float(degrees) + (float(minutes) / 60)
    dms = convert_to_dms(decimal_degrees)
    return dms


def convert_to_dms(decimal_degrees):
    # 将十进制度数转换为度分秒格式
    degrees = int(decimal_degrees)
    minutes = int((decimal_degrees - degrees) * 60)
    seconds = (decimal_degrees - degrees - minutes / 60) * 3600
    dms = f"{degrees}°{minutes}'{seconds:.2f}\""
    return dms


def get_gps_data(device, bote, flag):
    # ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)  # 串口号和波特率自行修改
    ser = serial.Serial(device, bote, timeout=1)  # winsows系统使用com1口连接串行口

    while True:
        """
        第一段程序读串口数据，utf-8 解析时候容易出现问题
        """
        try:
            # data = ser.readline().decode('utf-8')  # 读取串口数据
            data = ser.readline()  # 读取串口数据
            data = data.decode("utf-8")
            if data.startswith(flag):
                # print(data)
                lat = data.split(',')[2]
                lon = data.split(',')[4]
                alt = data.split(',')[9]
                lat = '4002.47081'
                lon = '11617.88324'
                alt = '40.28'
                # print("维度：" + lat, "经度：" + lon, "高程：" + alt)
                if lat and lon and alt:
                    lat = nmea0183_to_dms(lat)
                    lon = nmea0183_to_dms(lon)
                    print("维度：" + str(lat), "经度：" + str(lon), "高程：" + str(alt) + '\n')
            # print("******")
        except serial.SerialException:
            print('Error occurred')


if __name__ == '__main__':
    # get_gps_data('COM5', 4800, '$GPGGA')
    # get_gps_data('/dev/ttyUSB0', 4800, '$GPGGA')
    lat = '4002.47081'
    lon = '11617.88324'
    alt = '40.28'
    print(nmea0183_to_dms(lat))
    print(nmea0183_to_dms(lon))