# coding=utf-8
import struct
import ctypes
import time 
#import crc16
import datetime


mCRC16_Tables = [0, 4129, 8258, 12387, 16516, 20645, 24774, 28903, 33032, 37161, 41290, 45419, 49548, 53677, 57806,
                 61935, 4657, 528, 12915, 8786, 21173, 17044, 29431, 25302, 37689, 33560, 45947, 41818, 54205, 50076,
                 62463, 58334, 9314, 13379, 1056, 5121, 25830, 29895, 17572, 21637, 42346, 46411, 34088, 38153, 58862,
                 62927, 50604, 54669, 13907, 9842, 5649, 1584, 30423, 26358, 22165, 18100, 46939, 42874, 38681, 34616,
                 63455, 59390, 55197, 51132, 18628, 22757, 26758, 30887, 2112, 6241, 10242, 14371, 51660, 55789, 59790,
                 63919, 35144, 39273, 43274, 47403, 23285, 19156, 31415, 27286, 6769, 2640, 14899, 10770, 56317, 52188,
                 64447, 60318, 39801, 35672, 47931, 43802, 27814, 31879, 19684, 23749, 11298, 15363, 3168, 7233, 60846,
                 64911, 52716, 56781, 44330, 48395, 36200, 40265, 32407, 28342, 24277, 20212, 15891, 11826, 7761, 3696,
                 65439, 61374, 57309, 53244, 48923, 44858, 40793, 36728, 37256, 33193, 45514, 41451, 53516, 49453,
                 61774, 57711, 4224, 161, 12482, 8419, 20484, 16421, 28742, 24679, 33721, 37784, 41979, 46042, 49981,
                 54044, 58239, 62302, 689, 4752, 8947, 13010, 16949, 21012, 25207, 29270, 46570, 42443, 38312, 34185,
                 62830, 58703, 54572, 50445, 13538, 9411, 5280, 1153, 29798, 25671, 21540, 17413, 42971, 47098, 34713,
                 38840, 59231, 63358, 50973, 55100, 9939, 14066, 1681, 5808, 26199, 30326, 17941, 22068, 55628, 51565,
                 63758, 59695, 39368, 35305, 47498, 43435, 22596, 18533, 30726, 26663, 6336, 2273, 14466, 10403, 52093,
                 56156, 60223, 64286, 35833, 39896, 43963, 48026, 19061, 23124, 27191, 31254, 2801, 6864, 10931, 14994,
                 64814, 60687, 56684, 52557, 48554, 44427, 40424, 36297, 31782, 27655, 23652, 19525, 15522, 11395, 7392,
                 3265, 61215, 65342, 53085, 57212, 44955, 49082, 36825, 40952, 28183, 32310, 20053, 24180, 11923,
                 16050, 3793, 7920]

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


def init_crc16_tables(poly):
    re_crc16 = []
    for i in range(256):
        accum = (i << 8) & 0xFFFF
        for j in range(7, -1, -1):
            if (accum & 0x8000) != 0:
                accum = ((accum << 1) & 0xFFFF) ^ poly
            else:
                accum = accum << 1
        re_crc16.append(accum)
    return re_crc16
 
#crc16_table = init_crc16_tables(0x1021)


def crc16_table(bytestr):
    '''
    crc16查表法
    :param bytestr: bytes字符串
    :return: int16类型
    '''
    crc = 0x0000
    data = bytearray(bytestr)
    len1 = len(bytestr)
    for i in range(len1):
        cp = (crc >> 8) ^ data[i]
        crc = ((crc << 8) & 0xFFFF) ^ mCRC16_Tables[cp]
    return crc



def bcc(data):
    bcc = 0
    for i in range(len(data)):
        bcc ^= data[i]
    return bcc



#无人机回放数据
class Flight_REPLAY_Struct(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('s_cmd', ctypes.c_uint8),#子命令
        ('temp', ctypes.c_uint8),#温度
        ('eng',ctypes.c_uint8),#功耗
        ('v', ctypes.c_uint16),#电压
        ('a', ctypes.c_uint16),#电流
        ('PWM1', ctypes.c_uint16),
        ('PWM2', ctypes.c_uint16),
        ('PWM3', ctypes.c_uint16),
        ('PWM4', ctypes.c_uint16),
        ('PWM5', ctypes.c_uint16),
        ('PWM6', ctypes.c_uint16),
        ('PWM7', ctypes.c_uint16),
        ('PWM8', ctypes.c_uint16),
        ('PWM9', ctypes.c_uint16),
        ('PWM10', ctypes.c_uint16),
        ('offset_staus', ctypes.c_uint8),#差分状态
        ('lat', ctypes.c_int32),#纬度
        ('lon', ctypes.c_int32),#经度
        ('height', ctypes.c_uint16),#GPS高度
        ('rel_height', ctypes.c_int16),#相对原点高度x10
        ('real_height', ctypes.c_int16),#实时距地高度x10
        ('target_speed', ctypes.c_int16),#目标速度x100
        ('speed', ctypes.c_int16),#地速x100
        ('gps_speed', ctypes.c_uint16),#组合导航向速度X100
        ('trajectory', ctypes.c_int16),#轨迹角X10
        ('pitch', ctypes.c_int16),#俯仰角X100
        ('roll_angle', ctypes.c_int16),#横滚角角X100
        ('fu_wing', ctypes.c_int16),#副翼
        ('updown', ctypes.c_int16),#升降
        ('speedup', ctypes.c_int16),#油门
        ('toward', ctypes.c_int16),#方向
        ('lock',ctypes.c_uint8),#锁定
        ('toward_angle',ctypes.c_int16),#机头指向角
        ('fly_ctl',ctypes.c_uint8),#飞行控制模式
        ('staus',ctypes.c_uint16),#状态
        ('fly_status',ctypes.c_uint8),#飞行阶段
        ('gps_lost',ctypes.c_int8),#GPS丢星时间
        ('link_lost',ctypes.c_int8),#链路中断时间
        ('area',ctypes.c_uint16),#飞行区域
        ('turns_done',ctypes.c_uint8),#已飞行圈数
        ('turns_todo',ctypes.c_uint8),#等待飞行圈数
        ('fly_distance',ctypes.c_uint16),#飞行点距离
        ('fly_time',ctypes.c_uint16),#飞行时间
        ('target_point',ctypes.c_uint8),#目标航点
        ('target_height',ctypes.c_uint16),#目标高度
        ('target_angle',ctypes.c_uint16),#目标航向
        ('stay_time',ctypes.c_uint16),#悬停时间
        ('flyctl_v',ctypes.c_uint16),#飞控电压
        ('engine_v',ctypes.c_uint16),#动力电压
        ('gps_stars',ctypes.c_uint8),#GPS星数
        ('HDOP',ctypes.c_uint8),#水平精度HDOP
        ('VDOP',ctypes.c_uint8),#垂直精度VDOP
        ('SDOP',ctypes.c_uint8),#速度精度SDOP
        ('year',ctypes.c_uint8),#年
        ('month',ctypes.c_uint8),#月
        ('day',ctypes.c_uint8),#日
        ('hour',ctypes.c_uint8),#时
        ('min',ctypes.c_uint8),#分
        ('sec',ctypes.c_uint8),#秒
        ('flyctl_temp',ctypes.c_uint8),#飞控温度
        ('offset_dist',ctypes.c_uint16),#侧偏距
        ('channel_1',ctypes.c_uint16),
        ('channel_2',ctypes.c_uint16),
        ('channel_3',ctypes.c_uint16),
        ('channel_4',ctypes.c_uint16),
        ('channel_5',ctypes.c_uint16),
        ('channel_6',ctypes.c_uint16),
        ('height_cm',ctypes.c_uint16),#高度厘米位
        ('ms',ctypes.c_uint16),
        ('cmd_back1',ctypes.c_uint8),#指令返回值1
        ('cmd_back2',ctypes.c_uint8),#指令返回值2
        ('crc',ctypes.c_uint16),#crc16
        ('end',ctypes.c_uint8),#0xaa
        ('aa',ctypes.c_uint8),#0xaa
        ('bb',ctypes.c_uint8),#0xaa
    ]

    def CheckCRC(self,buffer,to_crc):
        getcrc = buffer[2:124]
        crc = crc16_table(getcrc)
        print(hex(crc))
        print(hex(to_crc))
        if to_crc == crc:
            return True
        else:
            return False


#无人机飞行实时数据
class Flight_Struct(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_uint8),#head
        ('head2', ctypes.c_uint8),#head2
        ('length', ctypes.c_uint8),#长度
        ('cmd', ctypes.c_uint8),#命令
        ('s_cmd', ctypes.c_uint8),#子命令
        ('temp', ctypes.c_uint8),#温度
        ('eng',ctypes.c_uint8),#功耗
        ('v', ctypes.c_uint16),#电压
        ('a', ctypes.c_uint16),#电流
        ('PWM1', ctypes.c_uint16),
        ('PWM2', ctypes.c_uint16),
        ('PWM3', ctypes.c_uint16),
        ('PWM4', ctypes.c_uint16),
        ('PWM5', ctypes.c_uint16),
        ('PWM6', ctypes.c_uint16),
        ('PWM7', ctypes.c_uint16),
        ('PWM8', ctypes.c_uint16),
        ('PWM9', ctypes.c_uint16),
        ('PWM10', ctypes.c_uint16),
        ('offset_staus', ctypes.c_uint8),#差分状态
        ('lat', ctypes.c_int32),#纬度
        ('lon', ctypes.c_int32),#经度
        ('height', ctypes.c_uint16),#GPS高度
        ('rel_height', ctypes.c_int16),#相对原点高度x10
        ('real_height', ctypes.c_int16),#实时距地高度x10
        ('target_speed', ctypes.c_int16),#目标速度x100
        ('speed', ctypes.c_int16),#地速x100
        ('gps_speed', ctypes.c_uint16),#组合导航向速度X100
        ('trajectory', ctypes.c_int16),#轨迹角X10
        ('pitch', ctypes.c_int16),#俯仰角X100
        ('roll_angle', ctypes.c_int16),#横滚角角X100
        ('fu_wing', ctypes.c_int16),#副翼
        ('updown', ctypes.c_int16),#升降
        ('speedup', ctypes.c_int16),#油门
        ('toward', ctypes.c_int16),#方向
        ('lock',ctypes.c_uint8),#锁定
        ('toward_angle',ctypes.c_int16),#机头指向角
        ('fly_ctl',ctypes.c_uint8),#飞行控制模式
        ('staus',ctypes.c_uint16),#状态
        ('fly_status',ctypes.c_uint8),#飞行阶段
        ('gps_lost',ctypes.c_int8),#GPS丢星时间
        ('link_lost',ctypes.c_int8),#链路中断时间
        ('area',ctypes.c_uint16),#飞行区域
        ('turns_done',ctypes.c_uint8),#已飞行圈数
        ('turns_todo',ctypes.c_uint8),#等待飞行圈数
        ('fly_distance',ctypes.c_uint16),#飞行点距离
        ('fly_time',ctypes.c_uint16),#飞行时间
        ('target_point',ctypes.c_uint8),#目标航点
        ('target_height',ctypes.c_uint16),#目标高度
        ('target_angle',ctypes.c_uint16),#目标航向
        ('stay_time',ctypes.c_uint16),#悬停时间
        ('flyctl_v',ctypes.c_uint16),#飞控电压
        ('engine_v',ctypes.c_uint16),#动力电压
        ('gps_stars',ctypes.c_uint8),#GPS星数
        ('HDOP',ctypes.c_uint8),#水平精度HDOP
        ('VDOP',ctypes.c_uint8),#垂直精度VDOP
        ('SDOP',ctypes.c_uint8),#速度精度SDOP
        ('year',ctypes.c_uint8),#年
        ('month',ctypes.c_uint8),#月
        ('day',ctypes.c_uint8),#日
        ('hour',ctypes.c_uint8),#时
        ('min',ctypes.c_uint8),#分
        ('sec',ctypes.c_uint8),#秒
        ('flyctl_temp',ctypes.c_uint8),#飞控温度
        ('offset_dist',ctypes.c_uint16),#侧偏距
        ('channel_1',ctypes.c_uint16),
        ('channel_2',ctypes.c_uint16),
        ('channel_3',ctypes.c_uint16),
        ('channel_4',ctypes.c_uint16),
        ('channel_5',ctypes.c_uint16),
        ('channel_6',ctypes.c_uint16),
        ('height_cm',ctypes.c_uint16),#高度厘米位
        ('ms',ctypes.c_uint16),
        ('cmd_back1',ctypes.c_uint8),#指令返回值1
        ('cmd_back2',ctypes.c_uint8),#指令返回值2
        ('crc',ctypes.c_uint16),#crc16
        ('end',ctypes.c_uint8),#0xaa
        ('aa',ctypes.c_uint8),#0xaa
        ('bb',ctypes.c_uint8),#0xaa
    ]


#无人机导航上传
class Flight_Course_Struct(ctypes.LittleEndianStructure):
    _fields_=[
        ('head', ctypes.c_ubyte),#head
        ('head2', ctypes.c_ubyte),#head2
        ('length', ctypes.c_ubyte),#长度
        ('cmd', ctypes.c_ubyte),#命令
        ('s_cmd', ctypes.c_ubyte),#子命令
        ('group', ctypes.c_ubyte),#航点组别
        ('lat', ctypes.c_float),#纬度X10^7上传
        ('lon', ctypes.c_float),#经度X10^7上传
        ('height', ctypes.c_float),#GPS高度×1000上传
        ('speed',ctypes.c_ushort),#速度×100上传
        ('stay_time',ctypes.c_ushort),#悬停时间
        ('radius',ctypes.c_ushort),#半径×10
        ('count',ctypes.c_ushort),#航点总数
        ('index',ctypes.c_ushort),#航点序号，从01开始
        ('att1',ctypes.c_ubyte),#Bit0:1:拍照0:不拍照Bit1: 1: 工作点0:降落点（待确认）(现象显示，1是降落点，0是工作点-0324)
        ('att2',ctypes.c_ubyte),#日bit0:0整条航线1单条航线bit1~2:00悬停转弯 01内切转弯1011预留--0408
        ('crc',ctypes.c_ushort),#crc16
        ('end',ctypes.c_ubyte),#0xaa
        
    ]


    def bitSet(self,byte,offset,value):
        if  value == 1:
            byte |=(1<<offset)
        elif value == 0:
            byte &=(~(1<<offset))
        return byte
    
    def photoset(self,byte,offset,value):
        if  value == "1":
            byte |=(1<<offset)
        elif value == "0":
            byte &=(~(1<<offset))
        return byte
        
    
    def double_bitSet(self,byte,offset,value):
        if  value == "00":
            byte &=(~(1<<offset))
            byte &=(~(1<<(offset-1)))
        elif value == "01":
            byte &=(~(1<<offset))
            byte |=(1<<(offset-1))
        elif value == "10":
            byte |=(1<<offset)
            byte &=(~(1<<(offset-1)))
        return byte


    
    def PathUpdate(self,lon,lat,height,speed,hovertime,radius,photo,heightmode,turning,totalnum,num):
        data =bytearray(33)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x21
        data[3]=0x05
        data[4]=0x41
        data[5]=0x00
        Lat = struct.pack("i", int(lat*(10**7)))  
        data[6]=Lat[0]
        data[7]=Lat[1]
        data[8]=Lat[2]
        data[9]=Lat[3]
        Lon = struct.pack("i", int(lon*(10**7)))  
        data[10]=Lon[0]
        data[11]=Lon[1]
        data[12]=Lon[2]
        data[13]=Lon[3]
        Height = struct.pack("I", int(height*1000))  
        data[14]=Height[0]
        data[15]=Height[1]
        data[16]=Height[2]
        data[17]=Height[3]
        Speed = struct.pack("H", speed*100)
        data[18]=Speed[0]
        data[19]=Speed[1]
        Hovertime = struct.pack("H", hovertime)  
        data[20]=Hovertime[0]
        data[21]=Hovertime[1]
        Radius = struct.pack("H", radius*10)  
        data[22]=Radius[0]
        data[23]=Radius[1]
        Totalnum = struct.pack("H", totalnum)
        data[24]=Totalnum[0]
        data[25]=Totalnum[1]
        Num = struct.pack("H", num)
        data[26]=Num[0]
        data[27]=Num[1]
        att1= 0x00
        att1= self.photoset(att1,7,photo)
        att1= self.double_bitSet(att1,1,heightmode)
        data[28]=att1
        att2= 0x00
        att2= self.double_bitSet(att2,6,turning)
        data[29]=att2
        crcstring = data[2:30]
        crc = crc16_table(crcstring)
        data[30]=crc&0xff
        data[31]=(crc>>8)&0xff
        data[32]=0xaa
        # print(data.hex())
        return data





    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))

    # def write_to_buffer(buffer, data, offset=0):
    #     if isinstance(buffer, ctypes.POINTER(ctypes.c_byte)):
    #         print("sss")
    #         ctypes.memmove(buffer, data, len(data))
    #         return

    
    def GetSend(self):
        data =bytearray(0x21)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x41
        self.end =0xaa

        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(data)
        self.crc = 0x11
        print ("crc %x "%crc)
        self.Print()
        ctypes.memmove(ptr1, ctypes.addressof(self), 0x21)
        print ("data %s "%data)
        #do data;

        

#无人机导航下传
class Flight_Course_Query(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_uint8),#head
        ('head2', ctypes.c_uint8),#head2
        ('length', ctypes.c_uint8),#长度
        ('cmd', ctypes.c_uint8),#命令
        ('s_cmd', ctypes.c_uint8),#子命令
        ('group', ctypes.c_uint8),#航点组别
        ('lat', ctypes.c_int32),#纬度X10^7上传
        ('lon', ctypes.c_int32),#经度X10^7上传
        ('height', ctypes.c_int32),#GPS高度×1000上传
        ('speed',ctypes.c_uint16),#速度×100上传
        ('stay_time',ctypes.c_uint16),#悬停时间
        ('radius',ctypes.c_uint16),#半径×10
        ('count',ctypes.c_uint16),#航点总数
        ('index',ctypes.c_uint16),#航点序号，从01开始
        ('att1',ctypes.c_uint8),#Bit0:1:拍照0:不拍照Bit1: 1: 工作点0:降落点（待确认）(现象显示，1是降落点，0是工作点-0324)
        ('att2',ctypes.c_uint8),#日bit0:0整条航线1单条航线bit1~2:00悬停转弯 01内切转弯1011预留--0408
        ('crc',ctypes.c_uint16),#crc16
        ('end',ctypes.c_uint8),#0xaa
        
    ]

    def PathQuery(self,totalnum,num):
        data =bytearray(33)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x21
        data[3]=0x05
        data[4]=0x42
        data[5]=0x00
        Totalnum = struct.pack("H", totalnum)
        data[24]=Totalnum[0]
        data[25]=Totalnum[1]
        Num = struct.pack("H", num)
        data[26]=Num[0]
        data[27]=Num[1]
        crcstring = data[2:30]
        crc = crc16_table(crcstring)
        data[30]=crc&0xff
        data[31]=(crc>>8)&0xff
        data[32]=0xaa
        # print(data.hex())
        return data






#定点导航设置
class Course_Set_Struct(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head
        ('head2', ctypes.c_ubyte),#head2
        ('length', ctypes.c_ubyte),#长度
        ('cmd', ctypes.c_ubyte),#命令
        ('s_cmd', ctypes.c_ubyte),#子命令
        ('type', ctypes.c_ubyte),#盘旋点类型
        ('lat', ctypes.c_float),#纬度X10^7上传
        ('lon', ctypes.c_float),#经度X10^7上传
        ('height', ctypes.c_ushort),#GPS高度×1000上传
        ('radius',ctypes.c_ushort),#半径×10
        ('time',ctypes.c_ubyte),#时间/圈数
        ('direction',ctypes.c_ubyte),#方向  00逆时针 01顺时针
        ('mode',ctypes.c_ubyte),# 00定点 01环绕
        ('speed',ctypes.c_ushort),#
        ('crc',ctypes.c_ushort),#crc16
        ('end',ctypes.c_ubyte),#0xaa
        
    ]

    def zero_one(self,byte,value):
        if  value == "00":
            byte = 0
        elif value == "01":
            byte = 1
        return byte
            

    #定点导航
    def point(self,lon,lat,height,radius,time,direction,mode,speed):
        data =bytearray(26)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x1a
        data[3]=0x05
        data[4]=0x02
        data[5]=0x00
        Lat = struct.pack("i", int(lat*(10**7)))  
        data[6]=Lat[0]
        data[7]=Lat[1]
        data[8]=Lat[2]
        data[9]=Lat[3]
        Lon = struct.pack("i", int(lon*(10**7)))  
        data[10]=Lon[0]
        data[11]=Lon[1]
        data[12]=Lon[2]
        data[13]=Lon[3]
        Height = struct.pack("H", int(height))  
        data[14]=Height[0]
        data[15]=Height[1]
        Radius = struct.pack("H", radius)  
        data[16]=Radius[0]
        data[17]=Radius[1]
        Time=struct.pack("B", int(time))
        data[18]=Time[0]
        aaa = 0x00
        data[19]=self.zero_one(aaa,direction) #0x00 逆时针 0x01 顺时针
        data[20]=self.zero_one(aaa,mode)  #0x00 定点 0x01 环绕
        Speed = struct.pack("H", speed)
        data[21]=Speed[0]
        data[22]=Speed[1]
        crcstring = data[2:23]
        crc = crc16_table(crcstring)
        data[23]=crc&0xff
        data[24]=(crc>>8)&0xff
        data[25]=0xaa       
        return data





    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))


    
    def GetSend(self,angle):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x02
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        return data
        #do data;



#航点确认指令
class Course_Confirm(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_uint8),#head
        ('head2', ctypes.c_uint8),#head2
        ('length', ctypes.c_uint8),#长度
        ('cmd', ctypes.c_uint8),#命令
        ('s_cmd', ctypes.c_uint8),#子命令
        ('next', ctypes.c_uint16),#下一个需要序号
        ('total',ctypes.c_uint16),#航点总数
        ('safe',ctypes.c_uint16),#类型（保留）
        ('crc',ctypes.c_uint16),#crc16
        ('end',ctypes.c_uint8),#0xaa
        
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))

    def PointComfirm(self,totalnum,num):
        data =bytearray(14)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x0e
        data[3]=0x05
        data[4]=0x22
        Totalnum = struct.pack("H", totalnum)
        data[7]=Totalnum[0]
        data[8]=Totalnum[1]
        Num = struct.pack("H", num)
        data[5]=Num[0]
        data[6]=Num[1]
        crcstring = data[2:11]
        crc = crc16_table(crcstring)
        data[11]=crc&0xff
        data[12]=(crc>>8)&0xff
        data[13]=0xaa 
        return data
    
    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x02
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;




#巡航圈数上传指令
class Flight_Circle_Struct(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head
        ('head2', ctypes.c_ubyte),#head2
        ('length', ctypes.c_ubyte),#长度
        ('cmd', ctypes.c_ubyte),#命令
        ('count', ctypes.c_ubyte),#圈数
        ('crc',ctypes.c_ushort),#crc16
        ('end',ctypes.c_ubyte),#0xaa
        
    ]

    #巡航圈数
    def turns(self,num):
        data =bytearray(8)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x08
        data[3]=0xcd
        data[4]=int(num)&0xff  #0 表示无线循环
        crcstring = data[2:5]
        crc = crc16_table(crcstring)
        data[5]=crc&0xff
        data[6]=(crc>>8)&0xff
        data[7]=0xaa
        print(data.hex())
        return data

    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))


    
    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x02
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;


#1.2飞行控制类
class Flight_Manage(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head
        ('head2', ctypes.c_ubyte),#head2
        ('length', ctypes.c_ubyte),#长度
        ('cmd', ctypes.c_ubyte),#命令
        ('s_cmd', ctypes.c_ubyte),#子命令
        ('ext_cmd', ctypes.c_ubyte),#命令扩展
        ('count', ctypes.c_ubyte),#盘旋点类型
        ('crc',ctypes.c_ushort),#crc16
        ('end',ctypes.c_ubyte),#0xaa
        
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))

    def Check(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf1
        data[4]=0x21
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        # print(data.hex())
        return data
        

    
    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0xF1
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;




#无人机心跳
class Flight_HeartBeat(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head
        ('head2', ctypes.c_ubyte),#head2
        ('length', ctypes.c_ubyte),#长度
        ('cmd', ctypes.c_ubyte),#命令
        ('s_cmd', ctypes.c_ubyte),#子命令
        ('crc',ctypes.c_ushort),#crc16
        ('end',ctypes.c_ubyte),#0xaa
        
    ]

    def SendHeartBeat(self):
        data =bytearray(8)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x08
        data[3]=0xa3
        data[4]=0xa3
        crcstring = data[2:5]
        crc = crc16_table(crcstring)
        data[5]=crc&0xff
        data[6]=(crc>>8)&0xff
        data[7]=0xaa
        return data
        
    


#无人机控制系统
class COM_JoyStick(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head aa
        ('head2', ctypes.c_ubyte),#head c8
        ('vertical', ctypes.c_ushort),#前进后退
        ('horizontal', ctypes.c_ushort),#方向摇杆值
        ('rising', ctypes.c_ushort),#油门摇杆
        ('roll',ctypes.c_ushort),#副翼摇杆值
        ('cam_angle',ctypes.c_ushort),#载荷俯仰
        ('cam_roll',ctypes.c_ushort),#载荷横滚
        ('cam_offset',ctypes.c_ushort),#载荷偏航
        ('takeshot',ctypes.c_ushort),#拍照按钮

    ]
    #发送控制
    def SendData(self):
        data =bytearray(16)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)

        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x16
        data[3]=0x07
        data[4]=0x01
        
        num_bytes = self.rising.to_bytes(2, byteorder='little')
        data[5]=num_bytes[0]
        data[6]=num_bytes[1]
        
        num_bytes = self.vertical.to_bytes(2, byteorder='little')
        data[7]=num_bytes[0]
        data[8]=num_bytes[1]
        
        num_bytes = self.rising.to_bytes(2, byteorder='little')
        data[9]=num_bytes[0]
        data[10]=num_bytes[1]

        num_bytes = self.horizontal.to_bytes(2, byteorder='little')
        data[11]=num_bytes[0]
        data[12]=num_bytes[1]
    
        crcstring = data[2:12]
        crc = crc16_table(crcstring)
        data[13]=crc&0xff
        data[14]=(crc>>8)&0xff
        data[15]=0xaa
        return data   



#1.2飞行动作指令
class Flight_Action(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head
        ('head2', ctypes.c_ubyte),#head2
        ('length', ctypes.c_ubyte),#长度
        ('cmd', ctypes.c_ubyte),#命令
        ('s_cmd', ctypes.c_ubyte),#子命令
        #   0x01: 起飞
        # 0x02: 返航
        # 0x05: 返回原点/回家降落

        # 0x07: 就地降落
        # 0x09: 解锁(动力启动，保持怠速)

        # 0x12: 开启夜航灯
        # 0x13: 关闭夜航灯

        # 0x28: 关车（加锁）
        # 0x29: 悬停
        # 0xF0：切换为遥控模式
        # 0xF1：切换为增稳模式（手控）
        # 0xF2：切换为全自主模式（程控）
        # 0xF3: 切换为定高模式
        ('ext_cmd', ctypes.c_ubyte),#命令扩展
        ('count', ctypes.c_ubyte),#盘旋点类型
        ('crc',ctypes.c_ushort),#crc16
        ('end',ctypes.c_ubyte),#0xaa
        
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))



    #解锁
    def Unlock(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0x09
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data

    #起飞
    def TakeOff(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0x01
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data
    
    #加锁
    def Lock(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0x28
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        # print(data.hex())
        return data
    
    #程控
    def AutomaticControl(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0xf2
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data   
    
    #手控
    def ManualControl(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0xf1
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        # print(data.hex())
        return data

    #回家降落
    def Return(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0x05
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data 
    
    
    #就地降落
    def Land(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0x07
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data 

    #打开防撞灯
    def Anticollision_Light_On(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0x12
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data 
    
    #关闭防撞灯
    def Anticollision_Light_Off(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0x13
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data 
    
    #打开遥控器
    def Controller_On(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0xe0
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data
    
    #关闭遥控器
    def Controller_Off(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0xe1
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        # print ("data %s "%data.hex())
        return data
    
    #打开双天线
    def Double_Antenna_On(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0x0A
        data[5]=0x01
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data    
    
    #关闭双天线
    def Double_Antenna_Off(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0x0A
        data[5]=0x00
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data  

    #获取磁偏角
    def MagneticDeclination(self):
        data =bytearray(9)
        data[0]=0xa5
        data[1]=0x5a
        data[2]=0x09
        data[3]=0xf3
        data[4]=0x0D
        data[5]=0x01
        crcstring = data[2:6]
        crc = crc16_table(crcstring)
        data[6]=crc&0xff
        data[7]=(crc>>8)&0xff
        data[8]=0xaa
        return data 



    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0xF3
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;


#飞机参数下传
class Flight_Param(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head
        ('head2', ctypes.c_ubyte),#head2
        ('length', ctypes.c_ubyte),#长度
        ('cmd', ctypes.c_ubyte),#命令
        ('s_cmd', ctypes.c_ubyte),#子命令
        ('mode', ctypes.c_ubyte),#缺省工作模式
        ('type', ctypes.c_ubyte),#机型类别标示
        ('subtype', ctypes.c_ubyte),#机型类别子标示
        ('param', ctypes.c_ushort),#机型参数
        ('max_height',ctypes.c_ushort),#最大工作高度
        ('normal_height',ctypes.c_ushort),#正常工作高度
        ('min_height',ctypes.c_ubyte),#最小工作高度
        ('parachute_height',ctypes.c_ubyte),#开伞高度
        ('parachute_height_safe',ctypes.c_ubyte),#开伞保护高度
        ('height',ctypes.c_ubyte),#离地高度
        ('safe_height',ctypes.c_ubyte),#起飞安全高度
        ('time',ctypes.c_ushort),#巡航时间
        ('parachute_open',ctypes.c_ubyte),#停车开伞时间
        ('two-wheeled_speed',ctypes.c_ushort),#两轮滑跑速度
        ('off_land_speed',ctypes.c_ushort),#离地速度
        ('off_land_speed',ctypes.c_ushort),#离地速度
        ('cruise_speed',ctypes.c_ushort),#巡航速度
        ('stall_speed',ctypes.c_ushort),#失速速度
        ('parachute_open_speed',ctypes.c_ushort),#开伞最大速度
        ('land_speed',ctypes.c_ushort),#降落下降速度
        ('Landing_speed',ctypes.c_ushort),#降落着陆速度
        ('max_climbing_angle',ctypes.c_ubyte),#最大爬升角
        ('max_dive_angle',ctypes.c_ubyte),#最大俯冲角
        ('max_roll_angle',ctypes.c_ubyte),#最大横滚角
        ('min_turn_angle',ctypes.c_ubyte),#最小转弯角
        ('throttle_mode',ctypes.c_ubyte),#油门控制方式
        # 0x00 直接控制
        # 0x01 转速控制
        # 0x02 空速控制
        ('throttle_takeoff',ctypes.c_ubyte),#起飞油门
        ('throttle_cruise',ctypes.c_ubyte),#巡航油门
        ('throttle_protect',ctypes.c_ubyte),#保护油门
        ('takeoff_mode',ctypes.c_ubyte),#起飞模式
        ('takeoff_param',ctypes.c_ubyte),#起飞参数
        ('takeoff_param2',ctypes.c_ushort),#起飞参数2
        ('landing_mode',ctypes.c_ubyte),#降落模式
        ('landing_param',ctypes.c_ubyte),#降落参数1
        ('landing_param2',ctypes.c_ubyte),#降落参数2
        ('landing_param2',ctypes.c_ushort),#降落航线长度
        ('landing_param2',ctypes.c_ushort),#降落航线宽度
        ('landing_param2',ctypes.c_ushort),#无动力滑行系数
        ('crc',ctypes.c_ushort),#crc16
        ('end',ctypes.c_ubyte),#0xaa
        
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))


    
    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x02
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ct5a09f30900edf3aaypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;


#吊舱系统
#2吊舱发送至软件命令帧
class Pod_Receive(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_uint8),#head
        ('head2', ctypes.c_uint8),#head2
        ('type', ctypes.c_uint8),#载荷
# 1：白光  2：红外  
# 3：双光  4：三光
        ('check', ctypes.c_uint8),#自检结果
#Bit0：红外机芯：   置1正常，0异常。
# Bit1：可见光机芯： 置1正常，0异常。
# Bit2：陀螺仪数据： 置1正常，0异常。
# Bit3：角度传感器： 置1正常，0异常。
# Bit4：驱动板：     置1正常，0异常。
# Bit5：压缩存储：   置1正常，0异常。
# Bit6：综合处理：   置1正常，0异常。
# Bit7：吊舱准备状态：置1载荷准备好，置0载荷未准备好
        ('pod_1', ctypes.c_uint16),#吊舱1
# Bit0：0：备用；
# Bit1：0：未视频抓图，1：正在视频抓图；
# Bit2：0：备用；
# Bit3：0：未视频连续抓图，1：正在视频连续抓图；
# Bit4：0：未开始录像，1：正在录像；
# Bit5：备用；
# Bit6：1：TF卡已插卡，0：TF卡未插卡；
# Bit7: 超温报警状态：0-未超温，1-超温；（测温红外）
# Bit8：备用；
# Bit9: 备用；
# Bit10～Bit13: 红外图像增强0~7；
# Bit14～Bit15: 图像显示模式；
        ('pod_2', ctypes.c_uint16),#吊舱2
# Bit0：备用
# Bit1：0：跟踪源为红外，1：跟踪源为可见光；
# Bit2~ Bit8：红外电子变倍倍数x10；
# Bit9：备用；
# Bit10~Bit11：可见光电子放大0-1 x; 1-2 x; 2-4x；
# Bit12～Bit15:色带；
        ('servo', ctypes.c_uint8),#伺服状态
# 0x01：载荷关
# 0x02: 手动
# 0x03: 收藏    bytestr = b'This is test string.'
# 0x07: 跟踪
# 0x08: 垂直下视
# 0x09:陀螺自动较漂
# 0x0A:陀螺温度较漂
# 0x0B:航向随动
# 0x0C:归中
# 0x0F:姿态指引
        ('pod_dir_angle', ctypes.c_uint16),#吊舱框架方位角×100倍
        ('pod_pitch', ctypes.c_uint16), #吊舱框架俯仰角×100倍
        ('pod_roll',ctypes.c_uint16),   #吊舱框架横滚角×100倍
        ('version',ctypes.c_uint8),     #当前载荷版本号A、B
        ('infrared_angle',ctypes.c_uint16),#红外视场角×10倍
        ('tf_usage',ctypes.c_uint8),     #TF使用容量百分比
        ('visual_angle',ctypes.c_uint16),#可见光视场角×10倍
        ('tf_total',ctypes.c_uint16),   #TF卡总容量×10倍
        ('infrared_focal_length',ctypes.c_uint16),  #红外焦距×10倍
        ('visual_focalcrcstring = self.crc = 0x11_length',ctypes.c_uint16),    #白光焦距×10倍
        ('infrared_distance',ctypes.c_uint16),      #激光测距距离×10倍
        ('lon', ctypes.c_float),#目标经度
        ('lat', ctypes.c_float),#目标纬度
        ('target_height',ctypes.c_int16),#目标海拔高度
        ('temp',ctypes.c_int16),#温度×10倍
        ('bak1',ctypes.c_uint16),#×100倍
        ('bak2',ctypes.c_uint16),#×100倍
        ('bak3',ctypes.c_uint16),#×100倍
        ('cur_image_type',ctypes.c_uint16),#当前显示图像反馈0：红外；1：可见光；
        ('cmd_recv',ctypes.c_uint16),#接收到的命令字反馈
        ('gest_recv',ctypes.c_uint16),#姿态指示完成反馈0x12：姿态指示中 0x13：姿态指示完成
        ('bak_s1',ctypes.c_uint16),#备用
        ('bak_s2',ctypes.c_uint16),#备用
        ('bak_s3',ctypes.c_uint16),#备用
        ('bak_s4',ctypes.c_uint16),#备用
        ('bak_s5',ctypes.c_uint16),#备用
        ('bak_s6',ctypes.c_uint16),#预留默认0
        ('crc',ctypes.c_uint8),#3～62字节异或校验低8位 
        ('end',ctypes.c_uint8),
        # self.crc = 0x11c_ubyte),#0xaa
        
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))


    
    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x02
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;




#吊舱控制指令return data
#2吊舱发送至软件命令帧
class Pod_Send(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_uint8),#head FB
        ('head2', ctypes.c_uint8),#head2 2A
        ('param1', ctypes.c_uint8*2),#参数A
        ('param2', ctypes.c_uint8*2),#参数B
        ('data', ctypes.c_uint8*30),#经常是飞控遥测参数
        ('ctl',ctypes.c_uint16),#云台摇杆指令
        ('ctl_param1',ctypes.c_uint16),#云台摇杆控制参数
        ('ctl_param1',ctypes.c_uint16),#云台摇杆控制参数
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x "%(self.head,self.head2))

    #视场上移  
    def FieldUp(self):
        data =bytearray(44)
        gtime = time.localtime() 
        data[0]=0xfb
        data[1]=0x2c
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec    
        data[37]=0x70
        data[40]=0x14
        data[41]=0x00         
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        # print(data)
        return data
    
    def test(self):
        data =bytearray(44)
        gtime = time.localtime() 
        data[0]=0xfb
        data[1]=0x2c
        data[7] =0x32
        data[9] =0x32
        data[11] =0x32
        data[13] =0x17
        data[14] =0x04
        data[15] =0x03
        data[16] =0x14
        data[17] =0x02
        data[18] =0x2b
        data[19] =0x23
        data[37]=0x70
        data[40]=0xfa
        data[41]=0xff
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        # print(data.hex())
        return data
        
    
    #视场下移  
    def FieldDown(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[37]=0x70
        data[40]=0xec
        data[41]=0xff         
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #视场左移  
    def FieldLeft(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[37]=0x70
        data[38]=0xec
        data[39]=0xff        
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #视场右移  
    def FieldRight(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[37]=0x70
        data[38]=0x14
        data[39]=0x00        
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #摄像头归中
    def Centering(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x71
        data[3]=0x00
        # data[11]=0x88
        # data[12]=0x45
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[37]=0x00
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    
    #摄像头归中test
    def Centeringtest(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x71
        data[3]=0x00
        data[11]=0x88
        data[12]=0x45
        data[13] =0x17
        data[14] =0x0b
        data[15] =0x16
        data[16] =0x11
        data[17] = 0x19
        data[18] =0x34
        data[19] =0x4f
        data[20] =0x14
        data[21] =0xda
        data[22] =0xe4
        data[23] = 0x42
        data[24] =0xd5
        data[25] =0x03
        data[26] =0xf4
        data[27] =0x41
        data[28] =0x00
        data[29] = 0x38
        data[37]=0x60
        data[42]=0x96
        data[43]=0xf0
        return data
    
    #拍照 
    def Photo(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x34
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #录像
    def Video(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x33
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data

    #视场放大
    def LargenField(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x45
        data[3]=0x01
        data[4]=0x07
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #视场减小
    def ReduceField(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x45
        data[3]=0x02
        data[4]=0x07
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #焦距+
    def FocusUp(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x45
        data[3]=0x03
        data[4]=0x03
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data

    #焦距-
    def FocusDown(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x45
        data[3]=0x04
        data[4]=0x03
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #停止变倍/变焦
    def Stop(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x45
        data[3]=0x00
        data[4]=0x00
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
        

    #开启激光测距
    def OpenLaser(self,pitch,roll_angle,toward_angle,lon,lat,height,rel_height):
        gtime = time.localtime()
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x3e
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        #俯仰角
        str = struct.pack("h", pitch)
        data[7]=str[0]
        data[8]=str[1]
        #滚转角
        str1 = struct.pack("h", roll_angle)  
        data[9]=str1[0]
        data[10]=str1[1]
        #航向角
        str2 = struct.pack("h", toward_angle)  
        data[11]=str2[0]
        data[12]=str2[1]
        #经度
        str3 = struct.pack("f", lon/10000000)
        data[20]=str3[0]
        data[21]=str3[1]
        data[22]=str3[2]
        data[23]=str3[3]
        #纬度
        str4 = struct.pack("f", lat/10000000)  
        data[24]=str4[0]
        data[25]=str4[1]
        data[26]=str4[2]
        data[27]=str4[3]
        #gps高度
        str5 = struct.pack("H", height)  
        data[29]=str5[0]
        data[30]=str5[1]
        #相对起飞点高度
        str6 = struct.pack("h", int(rel_height/10))  
        data[35]=str6[0]
        data[36]=str6[1]
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #关闭激光测距
    def CloseLaser(self,pitch,roll_angle,toward_angle,lon,lat,height,rel_height):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x3f
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        #俯仰角
        str = struct.pack("h", pitch)
        data[7]=str[0]
        data[8]=str[1]
        #滚转角
        str1 = struct.pack("h", roll_angle)  
        data[9]=str1[0]
        data[10]=str1[1]
        #航向角
        str2 = struct.pack("h", toward_angle)  
        data[11]=str2[0]
        data[12]=str2[1]
        #经度
        str3 = struct.pack("f", lon/10000000)
        data[20]=str3[0]
        data[21]=str3[1]
        data[22]=str3[2]
        data[23]=str3[3]
        #纬度
        str4 = struct.pack("f", lat/10000000)
        data[24]=str4[0]
        data[25]=str4[1]
        data[26]=str4[2]
        data[27]=str4[3]
        #gps高度
        str5 = struct.pack("H", height)  
        data[29]=str5[0]
        data[30]=str5[1]
        #相对起飞点高度
        str6 = struct.pack("h", int(rel_height/10))  
        data[35]=str6[0]
        data[36]=str6[1]
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data

    #跟踪
    def Tracking(self,pitch,roll_angle,toward_angle,lon,lat,height,rel_height):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x3a
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        #俯仰角
        str = struct.pack("h", pitch)
        data[7]=str[0]
        data[8]=str[1]
        #滚转角
        str1 = struct.pack("h", roll_angle)  
        data[9]=str1[0]
        data[10]=str1[1]
        #航向角
        str2 = struct.pack("h", toward_angle)  
        data[11]=str2[0]
        data[12]=str2[1]
        #经度
        str3 = struct.pack("f", lon/10000000)
        data[20]=str3[0]
        data[21]=str3[1]
        data[22]=str3[2]
        data[23]=str3[3]
        #纬度
        str4 = struct.pack("f", lat/10000000)
        data[24]=str4[0]
        data[25]=str4[1]
        data[26]=str4[2]
        data[27]=str4[3]
        #gps高度
        str5 = struct.pack("H", height)  
        data[29]=str5[0]
        data[30]=str5[1]
        #相对起飞点高度
        str6 = struct.pack("h", int(rel_height/10))  
        data[35]=str6[0]
        data[36]=str6[1]
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #收藏
    def Collect(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x74
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data

    #下视
    def Downward(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x73
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #扫描
    def Scanning(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x79
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #图像切换
    def ImageSwitch(self):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[2]=0x31
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data
    
    #摄像头心跳
    def Cambeat(self,pitch,roll_angle,toward_angle,lon,lat,height,rel_height,gps_stars):
        gtime = time.localtime() 
        data =bytearray(44)
        data[0]=0xfb
        data[1]=0x2c
        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec  
        #俯仰角
        str = struct.pack("h", pitch)
        data[7]=str[0]
        data[8]=str[1]
        #滚转角
        str1 = struct.pack("h", roll_angle)  
        data[9]=str1[0]
        data[10]=str1[1]
        #航向角
        str2 = struct.pack("h", toward_angle)  
        data[11]=str2[0]
        data[12]=str2[1]
        #经度
        str3 = struct.pack("f", lon/10000000)
        data[20]=str3[0]
        data[21]=str3[1]
        data[22]=str3[2]
        data[23]=str3[3]
        #纬度
        str4 = struct.pack("f", lat/10000000) 
        data[24]=str4[0]
        data[25]=str4[1]
        data[26]=str4[2]
        data[27]=str4[3]
        #gps高度
        str5 = struct.pack("H", height)  
        data[29]=str5[0]
        data[30]=str5[1]
        #相对起飞点高度
        str6 = struct.pack("h", int(rel_height/10))  
        data[35]=str6[0]
        data[36]=str6[1]
        #定位星数
        str7 = struct.pack("B", int(gps_stars))
        data[28]=str7[0]
        data[37]=0x60
        data[42]=bcc(data[2:42])
        data[43]=0xf0
        return data

    
    def GetSend(self):

        data =bytearray(44)
        # pi = ctypes.POINTER(data)
        # ptr1 = (ctypes.c_ubyte *42).from_buffer(data)
        # ptr1 = (ctypes.POINTER(ctypes.c_char)).from_address(ctypes.addressof(data)+2)
        # tmp = (ctypes.POINTER(ctypes.c_char)).from_address(ctypes.addressof(self)+2)
        gtime = time.gmtime() 
        data[0]=0xfb
        data[1]=0x2c
        data[2] =0x12
        # ctypes.memmove(ptr1, ctypes.addressof(self), 40)
        # ctypes.memmove(pif SelfCheck ==1 and Fight.Airport_Receive.battery_v < 44:



        data[13] =gtime.tm_year%100
        data[14] =gtime.tm_mon 
        data[15] =gtime.tm_mday
        data[16] =gtime.tm_hour
        data[17] =gtime.tm_min 
        data[18] =gtime.tm_sec

         
        # self.crc = 0x11
        #print ("str %s %x %d %d %d %d %d %d"%(crcstring,crc,gtime.tm_year,gtime.tm_mon,gtime.tm_mday,gtime.tm_hour,gtime.tm_min,gtime.tm_sec))
        #crc = crc16_table(crcstring)
        data[42]=bcc(data[2:42])
        data[43]=0xf0

        print ("data %s "%data)
        #do data;



#机场下传协议 0xc1
class Airport_Receive(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_uint8),#head aa
        ('head2', ctypes.c_uint8),#head2 c1
        ('length', ctypes.c_uint8),#length
        ('battery_v', ctypes.c_uint8),#电池电压
        ('battery_temp', ctypes.c_uint8),#电池温度
        ('wind_angle', ctypes.c_uint8),#风向
        #7	6	5	4	3	2	1	0
        #北风	东北风	东风	东南风	南风	西南风	西风	西北风
        ('rain_snow', ctypes.c_uint8),#雨雪传感器  1在下雨 0不在下雨
        ('out_temp', ctypes.c_int8),#舱外温度
        ('out_humidity', ctypes.c_int8),#舱外湿度
        ('in_temp', ctypes.c_int8),#舱内温度
        ('in_humidity', ctypes.c_int8),#舱内湿度
        ('warehouse_status', ctypes.c_uint8),#舱盖状态 0舱盖关闭 1正在打开 2已打开
        ('warehouse_angle', ctypes.c_uint8),#舱盖打开角度
        ('homing_status', ctypes.c_uint8),#归位机构状态 0锁定 1正在锁定 2打开 3正在打开
        ('battery_status', ctypes.c_uint8),#充电机状态  0电源断开 1电源打开
        ('uavpower_status', ctypes.c_uint32),#无人机电源状态 0无人机下电 1无人机上电
        ('bak1', ctypes.c_float),#预留
        ('bak2', ctypes.c_float),#预留
        ('bak3', ctypes.c_float),#预留
        ('bak4', ctypes.c_ubyte),#预留
        ('crc',ctypes.c_ushort),#crc16
        ('end',ctypes.c_ubyte),#0xaa
        
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))


    
    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x02
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;


#机场环境数据
class Airport_status(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head aa
        ('head2', ctypes.c_ubyte),#head2 c2
        ('length', ctypes.c_ubyte),#length
        ('wind_speed', ctypes.c_ushort),#风速x1000
        ('wind_angle', ctypes.c_ubyte),#风向
        #7	6	5	4	3	2	1	0
        #北风	东北风	东风	东南风	南风	西南风	西风	西北风
        ('rain_snow', ctypes.c_ubyte),#雨雪传感器
        ('out_temp', ctypes.c_float),#舱外温度
        #7	6	5	4	3	2	1	0
        #1温度为正值
        #0温度为负值	温度数据
        ('out_humidity', ctypes.c_float),#舱外湿度
        ('in_temp', ctypes.c_float),#舱内温度
        ('in_humidity', ctypes.c_float),#舱内湿度
        ('bak1', ctypes.c_float),#预留
        ('bak2', ctypes.c_float),#预留
        ('crc',ctypes.c_ubyte),#3～62字节异或校验低8位 
        ('end',ctypes.c_ubyte),#0xaa
        
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))


    
    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x02
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;


#1.4机场传感器数据-0xC4
class Airport_sensor(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head aa
        ('head2', ctypes.c_ubyte),#head2 c2
        ('length', ctypes.c_ubyte),#length
        ('x_val', ctypes.c_ushort),#X轴归位杆数据
        ('y_val', ctypes.c_ubyte),#Y轴归位数据
        ('ab_val', ctypes.c_ubyte),#A-B电动推杆数据
        ('cd_val', ctypes.c_ubyte),#A-C-D电动推杆数据
        ('x_pos', ctypes.c_float),#X轴归位杆所在位置
        ('y_pos', ctypes.c_float),#Y轴归位杆所在位置
        ('a_pos', ctypes.c_float),#A电动推杆所在位置
        ('b_pos', ctypes.c_float),#B电动推杆所在位置
        ('c_pos', ctypes.c_float),#C电动推杆所在位置
        ('d_pos', ctypes.c_float),#D电动推杆所在位置
        ('bak1', ctypes.c_float),#预留
        ('bak2', ctypes.c_float),#预留
        ('crc',ctypes.c_ubyte),#3～62字节异或校验低8位 
        ('end',ctypes.c_ubyte),#0xaa
        
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))


    
    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x02
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;

#机场运行心跳数据
class Airport_heartbeat(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head aa
        ('head2', ctypes.c_ubyte),#head2 c6
        ('length', ctypes.c_ubyte),#length
        ('warehouse_status', ctypes.c_ubyte),#舱盖状态
        ('warehouse_angle', ctypes.c_ubyte),#舱盖打开角度
        ('homing_status', ctypes.c_ubyte),#归位机构状态
        ('battery_status', ctypes.c_ubyte),#充电机状态
        ('uav_status', ctypes.c_ubyte),#无人机状态
        ('bak1', ctypes.c_float),#预留
        ('bak2', ctypes.c_float),#预留
        ('crc',ctypes.c_ushort),#crc16
        ('end',ctypes.c_ubyte),#0xaa
        
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))

    def Airportbeat(self):
        data =bytearray(18)
        data[0]=0xaa
        data[1]=0xc6
        data[2]=0x12
        # crcstring = data[2:6]
        # crc = crc16_table(crcstring)
        # data[6]=crc&0xff
        # data[7]=(crc>>8)&0xff
        crcstring = data[2:16]
        crc = crc16_table(crcstring)
        data[16]=crc&0xff
        data[17]=(crc>>8)&0xff
        data[18]=0xaa
        return data   
    

    
    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x02
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;



#机场上传协议
# 舱盖控制-0xd1
class Hatch_control(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head aa
        ('head2', ctypes.c_ubyte),#head2 d1
        ('length', ctypes.c_ubyte),#length
        ('warehouse_status', ctypes.c_ubyte),#舱盖状态  0关闭舱盖 1打开舱盖
        # ('homing_status', ctypes.c_ubyte),#归位机构控制  0锁定 1解锁
        # ('charge_ctl', ctypes.c_ubyte),#充电状态控制  0充电 1断开充电
        ('bak1', ctypes.c_float),#预留
        ('bak2', ctypes.c_float),#预留
        ('bak3', ctypes.c_float),#预留
        ('bak4', ctypes.c_float),#预留
        ('bak5', ctypes.c_float),#预留
        ('bak6', ctypes.c_float),#预留
        ('bak7', ctypes.c_ubyte),#预留
        ('crc',ctypes.c_ushort),#3～28字节异或校验低8位 
        ('end',ctypes.c_ubyte),#0xaa    
    ]
    # def __init__(self):
        # self.head   ='\x00'
        # self.head2  ='\x00'
        # self.length ='\0x21'
        # self.end ='\0xaa'
    def Print(self):
        print ("head :%x %x %d %x"%(self.head,self.head2,self.length,self.crc))

    # 关闭舱盖
    def CloseHatch(self):
        data =bytearray(32)
        data[0]=0xaa
        data[1]=0xd1
        data[2]=0x20
        data[3]=0x00
        crcstring = data[0:29]  
        crc = crc16_table(crcstring)
        data[29]=crc&0xff
        data[30]=(crc>>8)&0xff
        data[31]=0xaa
        # print(data.hex())
        return data   
    
       # test
    def test(self):
        data =bytearray(32)
        data[0]=0xaa
        data[1]=0xd1
        data[2]=0x20
        data[3]=0x00
        data[4]=0x18
        data[5]=0x02
        data[6]=0x00
        data[7]=0x13
        data[8]=0x24
        data[9]=0x17
        data[10]=0x20
        data[12]=0xb4
        # crcstring = data[2:6]
        # crc = crc16_table(crcstring)
        # data[6]=crc&0xff
        # data[7]=(crc>>8)&0xff
        crcstring = data[0:29]
        crc = crc16_table(crcstring)
        data[29]=crc&0xff
        data[30]=(crc>>8)&0xff
        data[31]=0xaa
        print(data.hex())
        return data   
    

    # 打开舱盖
    def OpenHatch(self):
        data =bytearray(32)
        data[0]=0xaa
        data[1]=0xd1
        data[2]=0x20
        data[3]=0x01
        crcstring = data[0:29]
        crc = crc16_table(crcstring)
        data[29]=crc&0xff
        data[30]=(crc>>8)&0xff
        data[31]=0xaa
        # print(data.hex())
        return data
    

#归位机构控制-0xd2
class Homing_control(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head aa
        ('head2', ctypes.c_ubyte),#head2 d1
        ('length', ctypes.c_ubyte),#length
        #('warehouse_status', ctypes.c_ubyte),#舱盖状态  0关闭舱盖 1打开舱盖
        ('homing_status', ctypes.c_ubyte),#归位机构控制  0锁定 1解锁
        # ('charge_ctl', ctypes.c_ubyte),#充电状态控制  0充电 1断开充电
        ('bak1', ctypes.c_float),#预留
        ('bak2', ctypes.c_float),#预留
        ('bak3', ctypes.c_float),#预留
        ('bak4', ctypes.c_float),#预留
        ('bak5', ctypes.c_float),#预留
        ('bak6', ctypes.c_float),#预留
        ('bak7', ctypes.c_ubyte),#预留
        ('crc',ctypes.c_ushort),#3～28字节异或校验低8位 
        ('end',ctypes.c_ubyte),#0xaa    
    ]
    # 归位锁定
    def HomeLock(self):
        data =bytearray(32)
        data[0]=0xaa
        data[1]=0xd2
        data[2]=0x20
        data[3]=0x00
        crcstring = data[0:29]
        crc = crc16_table(crcstring)
        data[29]=crc&0xff
        data[30]=(crc>>8)&0xff
        data[31]=0xaa
        # print(data.hex())
        return data    

    # 归位解锁
    def HomeUnlock(self):
        data =bytearray(32)
        data[0]=0xaa
        data[1]=0xd2
        data[2]=0x20
        data[3]=0x01
        crcstring = data[0:29]
        crc = crc16_table(crcstring)
        data[29]=crc&0xff
        data[30]=(crc>>8)&0xff
        data[31]=0xaa
        # print(data.hex())
        return data 


#充电控制-0xd3
class Charge_control(ctypes.LittleEndianStructure):
    _pack_=1
    _fields_=[
        ('head', ctypes.c_ubyte),#head aa
        ('head2', ctypes.c_ubyte),#head2 d1
        ('length', ctypes.c_ubyte),#length
        #('warehouse_status', ctypes.c_ubyte),#舱盖状态  0关闭舱盖 1打开舱盖
        #('homing_status', ctypes.c_ubyte),#归位机构控制  0锁定 1解锁
        ('charge_ctl', ctypes.c_ubyte),#充电状态控制  0充电 1断开充电
        ('bak1', ctypes.c_float),#预留
        ('bak2', ctypes.c_float),#预留
        ('bak3', ctypes.c_float),#预留
        ('bak4', ctypes.c_float),#预留
        ('bak5', ctypes.c_float),#预留
        ('bak6', ctypes.c_float),#预留
        ('bak7', ctypes.c_ubyte),#预留
        ('crc',ctypes.c_ushort),#3～28字节异或校验低8位 
        ('end',ctypes.c_ubyte),#0xaa    
    ]
    # 充电
    def Charge(self):
        data =bytearray(32)
        data[0]=0xaa
        data[1]=0xd3
        data[2]=0x20
        data[3]=0x00
        crcstring = data[0:29]
        crc = crc16_table(crcstring)
        data[29]=crc&0xff
        data[30]=(crc>>8)&0xff
        data[31]=0xaa
        # print(data.hex())
        return data

    # 断开充电
    def ChargeOff(self):
        data =bytearray(32)
        data[0]=0xaa
        data[1]=0xd3
        data[2]=0x20
        data[3]=0x01
        crcstring = data[0:29]
        crc = crc16_table(crcstring)
        data[29]=crc&0xff
        data[30]=(crc>>8)&0xff
        data[31]=0xaa
        # print(data.hex())
        return data     


    
    def GetSend(self):

        data =bytearray(0x1A)
        # pi = ctypes.POINTER(data)
        ptr1 = (ctypes.c_ubyte *self.length ).from_buffer(data)
        self.head  =0xa5
        self.head2 =0x5a
        self.cmd =0x05
        self.s_cmd =0x02
        self.end =0xaa
        
        # ctypes.memmove(ctypes.addressof(data), ctypes.addressof(self), ctypes.sizeof(self))
        # ptr1 = (ctypes.c_ubyte).from_buffer(data)

        #self.write_to_buffer(ptr1,self)
        

        crc = crc16_table(ptr1)
        self.crc = 0x11
        print ("crc %x "%(crc))
        self.Print()

        ctypes.memmove(ptr1, ctypes.addressof(self), 0x1A)
        print ("data %s "%data)
        #do data;


#测试指令数据

if __name__ == "__main__":    
    send = Flight_Course_Struct()
    print (">>>: %s "%(send.__class__.__name__ ))

    # send.GetSend()
    

    send = Course_Set_Struct()
    print (">>>: %s "%(send.__class__.__name__ ))
    # send.GetSend()
    
    send = Hatch_control()
    print (">>>: %s "%(send.__class__.__name__ ))
    send.test()
    
    