import socket
import struct
import ctypes
import json
import time 


class Flight_Struct(ctypes.LittleEndianStructure):
    _fields_=[
        # ('cmd', ctypes.c_ubyte),#命令
        # ('s_cmd', ctypes.c_ubyte),#子命令
        # ('temp', ctypes.c_ubyte),#温度
        # ('eng',ctypes.c_ubyte),#功耗
        # ('v', ctypes.c_short),#电压
        # ('a', ctypes.c_short),#电流
        # ('PWM1', ctypes.c_short),
        # ('PWM2', ctypes.c_short),
        # ('PWM3', ctypes.c_short),
        # ('PWM4', ctypes.c_short),
        # ('PWM5', ctypes.c_short),
        # ('PWM6', ctypes.c_short),
        # ('PWM7', ctypes.c_short),
        # ('PWM8', ctypes.c_short),
        # ('PWM9', ctypes.c_short),
        # ('PWM10', ctypes.c_short),
        # ('offset_staus', ctypes.c_ubyte),#差分状态
        ('lat', ctypes.c_float),#纬度
        ('lon', ctypes.c_float),#经度
        ('height', ctypes.c_short),#GPS高度
        ('rel_height', ctypes.c_short),#相对原点高度
        ('real_height', ctypes.c_short),#实时距地高度
        ('target_speed', ctypes.c_short),#目标速度
        ('speed', ctypes.c_short),#地速
        ('gps_speed', ctypes.c_short),#组合导航天向速度
        ('trajectory', ctypes.c_short),#轨迹角
        ('pitch', ctypes.c_short),#俯仰角
        ('roll_angle', ctypes.c_short),#横滚角角
        ('fu_wing', ctypes.c_ushort),#副翼
        ('updown', ctypes.c_ushort),#升降
        ('speedup', ctypes.c_ushort),#油门
        ('toward', ctypes.c_ushort),#方向
        ('lock',ctypes.c_ubyte),#锁定
        ('toward_angle',ctypes.c_short),#机头指向角
        ('fly_ctl',ctypes.c_ubyte),#飞行控制模式
        ('staus',ctypes.c_ushort),#状态
        ('fly_status',ctypes.c_ubyte),#飞行阶段
        ('gps_lost',ctypes.c_ubyte),#GPS丢星时间
        ('link_lost',ctypes.c_ubyte),#链路中断时间
        ('area',ctypes.c_ushort),#飞行区域
        ('turns_done',ctypes.c_ubyte),#已飞行圈数
        ('turns_todo',ctypes.c_ubyte),#等待飞行圈数
        ('fly_distance',ctypes.c_ushort),#飞行点距离
        ('fly_time',ctypes.c_ushort),#飞行时间
        ('target_point',ctypes.c_ubyte),#目标航点
        ('target_height',ctypes.c_ushort),#目标高度
        ('target_angle',ctypes.c_ushort),#目标航向
        ('stay_time',ctypes.c_ubyte),#悬停时间
        ('flyctl_v',ctypes.c_ushort),#飞控电压
        ('engine_v',ctypes.c_ushort),#动力电压
        ('gps_stars',ctypes.c_ubyte),#GPS星数
        ('HDOP',ctypes.c_ubyte),#水平精度HDOP
        ('VDOP',ctypes.c_ubyte),#垂直精度VDOP
        ('SDOP',ctypes.c_ubyte),#速度精度SDOP
        ('year',ctypes.c_ubyte),#年
        ('month',ctypes.c_ubyte),#月
        ('day',ctypes.c_ubyte),#日
        ('hour',ctypes.c_ubyte),#时
        ('min',ctypes.c_ubyte),#分
        ('sec',ctypes.c_ubyte),#秒
        ('flyctl_temp',ctypes.c_ubyte),#飞控温度
        ('offset_dist',ctypes.c_ushort),#侧偏距
    ]
    
class Network(object):  # 创建Circle类
    def __init__(self, ip,port,hang_ip,hang_port): # 初始化一个属性r（不要忘记self参数，他是类下面所有方法必须的参数）
        self.ip = ip  
        self.port = port  
        self.hang_ip = hang_ip  
        self.hang_port = hang_port  
       
        self.udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        # 2.绑定一个本地信息 
        localaddr = (self.ip,self.port) 
        # 必须绑定自己电脑IP和port 
        self.udp_socket.bind(localaddr) 
        
       
    def on_connect(self,client, userdata, flags, rc):
        if rc == 0 and client.is_connected():
            print("Connected to MQTT Broker!")
            client.subscribe(TOPIC)
        else:
            print(f'Failed to connect, return code {rc}')

    def on_disconnect(self,client, userdata, rc):
    #    logging.info("Disconnected with result code: %s", rc)
        print(f'Rec%s'%rc)
    def on_message(self,client, userdata, msg):
        print(f'Received `{msg.payload.decode()}` from `{msg.topic}` topic')
    def connect_mqtt(self):
        client = mqtt_client.Client(CLIENT_ID)
        client.username_pw_set(USERNAME, PASSWORD)
        client.on_connect = self.on_connect
        client.on_message = self.on_message
        client.connect(BROKER, PORT, keepalive=120)
        client.on_disconnect = self.on_disconnect
        return client
        
    def receivedata(self):
        # udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) 
        # # 2.绑定一个本地信息 
        # localaddr = ("192.168.8.200",14551) 
        # # 必须绑定自己电脑IP和port 
        # udp_socket.bind(localaddr) 
        a = int('a5',16)
        b = int('5a',16)
        cmd = int('10',16)

        # client = connect_mqtt()
        test = Flight_Struct()
        # 3.接收数据 
        while True: 
            data = self.udp_socket.recvfrom(1)
            head = struct.unpack("B", data)
            if a == int.from_bytes(head, byteorder='little'):
                # print("=0x%x "%(head))
                data = self.udp_socket.recvfrom(1)
                head2 = struct.unpack("B", data)
                if b == int.from_bytes(head2, byteorder='little'):
                    print("->0x%x"%(head2))
                    lenc = self.udp_socket.recvfrom(1)
                    len2 = struct.unpack("B", lenc)
                    len = int.from_bytes(len2, byteorder='little')
                    #left length
                    if(len == 128):
                        # self.udp_socket.recvfrom(len-3)
                        data = self.udp_socket.recvfrom(32-3)
                        left = len -32
                        # data = self.udp_socket.recvfrom(4)
                        # lat = struct.unpack("<i", data)
                        # data = self.udp_socket.recvfrom(4)
                        # lon = struct.unpack("<i", data)
                        # print("----len ---%s %s "%(lat,lon))
                        # left = len -3
                        data = self.udp_socket.recvfrom(left)

                    
                        # print("----len ---%d  %s"%(len,data))
                        ctypes.memmove(ctypes.addressof(test), data, ctypes.sizeof(test));
                        
                        msg_dict = {
                            'speed':test.speed/100,
                            'lat': test.lat/pow(10,7),
                            'lon': test.lon/pow(10,7),
                            'height': test.height/10,
                            'target_angle':test.target_angle/10
                        }
                        msg = json.dumps(msg_dict)

                        # lat = struct.unpack("<H",data[29],29)
                        # lon = struct.unpack("<H",data,33)
                        # print ("gps :%f %f"%(lat,lon))

                        # cmd,s_cmd,temp,eng,v,a,pw1,pw2,pw3,pw4,pw5,pw6,pw7,pw8,pw9,pw10,staus,lat,lon,height,pheight = struct.unpack("BBBBHHHHHHHHHHHHBffhh", data)
                        # print ("gps :%f %f %f %d"%(test.lat,test.lon,test.height,test.target_angle))

                        print ("--->gps %f %f %f %f %f"%(msg_dict['lat'],msg_dict['lon'],msg_dict['height'],msg_dict['speed'],msg_dict['target_angle']))


                        # result = client.publish(TOPIC, msg)
                        # result: [0, 1]
                        # status = result[0]
                        # if status == 0:
                        #     print(f'Send `{msg}` to topic `{TOPIC}`')
                        # else:
                        #     print(f'Failed to send message to topic {TOPIC}')


                        #告警信息显示
                        msg_dict = {
                            "id" :2,
                            "name" :"人员告警",
                            "image" :"/images/alert_image.jpg",
                            "type" :2,
                            "code" :"2222",
                            "level" :2,
                            "count" :10,
                            "platform" :2,
                            "start_time" : "2023-10-2 14:20:32",
                            "end_time" :"2023-10-2 13:10:12",
                            "note" :"人员闯入",
                            "lat" :23.22,
                            "lon" :23.22,
                            "alt" : 200.23,
                            "history_id" : 1,
                            "confirm" :0,
                        }
                        msg = json.dumps(msg_dict)

                        # result = client.publish(TOPIC_ALERT, msg)
                        # # result: [0, 1]
                        # status = result[0]
                        # if status == 0:
                        #     print(f'Send `{msg}` to topic `{TOPIC_ALERT}`')
                        # else:
                        #     print(f'Failed to send message to topic {TOPIC_ALERT}')
                    
                        # time.sleep(2)

        
            # recv_data = self.udp_socket.recvfrom(1024) 
            # # recv_data存储元组（接收到的数据，（发送方的ip,port）） 
            # recv_msg = recv_data[0] 
            # # 信息内容 
            # send_addr = recv_data[1] # 信息地址 
            # # 4.打印接收到的数据 
            # print(recv_data) 
            # print("信息来自:%s 内容是:%s" %(str(send_addr),recv_msg.decode("gbk"))) 
            # 5.退出套接字 
        self.udp_socket.close() 
    def Loop(self): 
        # 1创建套接字 
        while True:
            try:
                self. receivedata()
            except Exception as link_fault:
                print("网络异常:%s "% link_fault)
                self.udp_socket.close() 
                time.sleep(2)
                continue
        
if __name__ == "__main__": 
    network = Network("192.168.8.200",14551,"192.168.8.201",2222)
    network.receivedata()