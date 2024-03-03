from filecmp import cmp
import numbers
import os
import random
import socket
import struct
import ctypes
import json
import asyncio
import copy
import signal
from geopy.distance import geodesic
# import serial
import time
import webSocket.flight as Fight
# import webSocket.crc16 as crc16
import numpy as np
# import drone_yolov8_deploy_noshow as yolo
import argparse
# from paho.mqtt import client as mqtt_client
import threading
from gmqtt import Client as MQTTClient
import redis
from goto import with_goto
from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor
# from playsound import playsound

# import pygame
# pygame.init()
# pygame.mixer.init()
#判断对象是否存在
def isset(v):
   try :
     type (eval(v))
   except :
     return  0 
   else :
     return  1 
 

# 调用load_alarm_sound函数，加载警报音频
# load_alarm_sound("/javodata/drone_projects/alert.mp3")

BROKER = '127.0.0.1'
PORT = 1883
TOPIC_INFO = "info"
TOPIC_ALERT = "alert/#"
TOPIC_CONSOLE = "console" #命令数据
TOPIC_CTRL    = "control" #命令
TOPIC_STATE = "state"
FLY_CTRL = "fly_control"

rootpassword = "123456"

CLIENT_ID = f'pushuav222222'
USERNAME = ''
PASSWORD = ''

r = redis.Redis(host='127.0.0.1',port=6379,db=0)


#无人机
#经度
lon=0
#纬度 
lat=0 
#高度
height  =0

#默认网卡
eth="eth0"
#手柄设备
joystick="/dev/ttys0"


#前端控制播放位置 > 0
doSeek  =-1

#is main control device ， == 1 can send message，or only listen data
IsMaster =0
#自检
SelfCheck =0#1  0失败 1成功
# 心跳check
# self.HeartbeatCheck =0#1

camera_url ="" 

#无人机模式
mode  ="automatic" #auto manual
#防撞灯状态
light ="on" #on off
#激光测距状态
laser ="on" #on off
#无人机自检磁偏角
mc = 0.0
#当前飞行id


STOP = asyncio.Event()

flightPath=[]


# playsound('alarm.wav')
#打印输出端
def consolelog(msg):
    print(msg)
    if(mqttclient):
        mqttclient.publish(TOPIC_CONSOLE, ""+msg+"")



#auto
class AutoThread(threading.Thread):
    def __init__(self,path,historyid):
        super(AutoThread,self).__init__()
        self.path = path
        self.isStop =False
        self.isStart=False
        self.history_id = historyid
        uav.path_loaded = False

    def Stop(self):
        self.isStop = True

    def Next(self):
        self.isStop = False

    def run(self):
        # return
        if airport.airportdata.rain_snow == False:
            consolelog("气象正常")
        else:
            SendFlyOver(self.history_id,3,"气象问题,无法起飞")
            return

        
        print(airport.airportdata.homing_status)
#check airport status normal == 0 
        #if airport.airportdata.homing_status != 2: 
        if airport.airportdata.homing_status != 0: 
            SendFlyOver(self.history_id,3,"归机机构自检失败")
            return
        else:
            consolelog("归机机构正常")
        
#unlock airport

        if airport.airportdata.homing_status == 0: 
            #send unlock airport
            UnlockAirport() 
            

#wait unitle == 2 
        quit_time =0
        #normal use ==2
        # while(airport.airportdata.homing_status !=2):
        while(airport.airportdata.homing_status !=3):
            print(airport.airportdata.homing_status)
            quit_time +=1
            if quit_time > 30:
                SendFlyOver(self.history_id,3,"归机机构无法打开")
                return
            time.sleep(1)

        if airport.airportdata.battery_v >= 3:
        #no device ,use opening status =3 to run
            consolelog("机库电压正常")
        else:
            SendFlyOver(self.history_id,3,"机库电压异常,无法起飞 :")
            return

        
        # r.hset('drone','historyid',history_id)
        
        OpenAirport()
        consolelog("发送机场开仓指令")
        print(airport.airportdata.warehouse_status)
    #how long cang gai open 
        time.sleep(5)
        quit_time =0
        while(airport.airportdata.warehouse_status !=1):
            if airport.airportdata.warehouse_status == 1: 
                consolelog("舱盖已经打开")
                break
            quit_time +=1
            if quit_time > 40:
                SendFlyOver(self.history_id,3,"舱盖无法打开")
                return
            time.sleep(1)
        send_state()
        #发送航线数据
        # print('无人机定位数据' + str(uav.uavdata.lon) + "  "+str(uav.uavdata.lat) )
        consolelog('无人机定位数据 : ' + str(uav.uavdata.lon) + "  "+str(uav.uavdata.lat) )
#how long to stop the GPS
        quit_time =0
        while(uav.uavdata.lon == 0 and uav.uavdata.lat == 0 ):
            quit_time +=1
            if quit_time > 60*5:
                SendFlyOver(self.history_id,3,"定位失败,无法起飞")
                return
            time.sleep(1)
        
        # RunSelfCheck()
        consolelog("装订航线")
        # a =[path]
        # print (a)
    
        lon = uav.lon
        lat = uav.lat
        height = uav.height
        re = send_path(self.path)
        if re ==1:
            SendFlyOver(self.history_id,3,"装订航线失败,无法起飞")
            return
        consolelog("装订航线完成 ")
        time.sleep(5)


        consolelog("发送程控指令")
        SendProgramControl()
        send_state()

        consolelog('无人机解锁')
        # msg = b'{"cmd":"drone/unlock","data":"on"}'
        # mqttclient.publish(TOPIC_CTRL, msg)
        time.sleep(10)
        


        # 飞机飞行轨迹。
        # Takeoff()
        # pod = Fight.Flight_Action()
        # data =pod.TakeOff()
        # uav.Send(data)
        # r.hset(uav.id,'takeoff','off')
        consolelog("发送飞行指令")

#1 km to 
        # closeit =False
        # while (airport.airportdata.warehouse_status == 2 and closeit ==False):
        #     dist = geodesic((uav.lat,uav.lon), (lat,lon)).km   
        #     while(dist > 1):
        #         CloseAirport()
        #         closeit = True
        #         consolelog('关舱盖')
        #         break
                
        #     consolelog('舱盖是否开关' +airport.airportdata.warehouse_status)
        #     time.sleep(1)
#how to next 
        #返航状态 
        # while uav.uavdata.fly_status != 0x05:
        #     time.sleep(1)

        dist = geodesic((uav.lat,uav.lon), (lat,lon)).km  

#how long to open 1km
        #0.5 km 
        while(dist > 1):
             dist =  geodesic((uav.lat,uav.lon), (lat,lon)).km    
             consolelog('距离机场' + str(dist))
             time.sleep(1)

       
        consolelog('距离机库小于1km')
        OpenAirport()
        send_state()
        quit_time =0
        while(airport.airportdata.warehouse_status !=1):
            if airport.airportdata.warehouse_status == 1: 
                consolelog("舱盖已经打开")
                break
            quit_time +=1
            if quit_time > 40:
                SendFlyOver(self.history_id,3,"舱盖无法打开")
                return
            time.sleep(1)
        #降落
        #need check 
        time.sleep(5)
        consolelog('等待飞机降落')
#2 min  !!!!!! only real flight can go through
        quit_time =0
        while(uav.uavdata.lock == 0x09 or uav.uavdata.lock == 0x00):
            quit_time +=1
            time.sleep(1)
            if quit_time > 60*5:
                send_state()
                SendFlyOver(self.history_id,3,"飞机降失败")
                return
        

#aire port
#归位机构控制 2：锁定
        if airport.airportdata.homing_status == 2: 
            #send lock airport 
            
            SendFlyOver(self.history_id,3,"归机机构失败")
            return

#10
        # CloseAirport()
        # quit_time =0
        # while(airport.airportdata.homing_status != 0):
        #     quit_time +=1
        #     time.sleep(1)
        #     if quit_time > 10:
        #         SendFlyOver(self.history_id,3,"归机机构失败")
        #         return
            
        # if airport.airportdata.homing_status != 0: 
        #     SendFlyOver(self.history_id,3,"归机机构自检失败")
        #     return
        # else:
        #     consolelog("归机机构正常")
#close it    
        CloseAirport()

        consolelog('关闭机库')
        send_state()

#need check  close close airport 30s
        quit_time =0
        while(airport.airportdata.warehouse_status !=0):
            quit_time +=1
            if quit_time > 30:
                SendFlyOver(self.history_id,3,"舱盖关闭失败")
                return
            time.sleep(1)

        SendFlyOver(self.history_id,1,"任务完成")
        send_state()
        
#飞行结束，汇报数据
def SendFlyOver(history_id,status,data):
    consolelog(data)
    msg_dict ={"cmd":"fly_over","history_id":history_id,"fly_id":status,"data":data}
    msg = json.dumps(msg_dict)
    mqttclient.publish(FLY_CTRL, msg)
    # mqttclient.publish(TOPIC_CTRL, msg)
    if uav.doFlyFile is not None:
        uav.doFlyFile.close()
        uav.doFlyFile = None
    
#发送程控
def SendProgramControl():
    pod = Fight.Flight_Action()
    data =pod.AutomaticControl()
    consolelog("发送程控")
    uav.Send(data)  
    r.hset('drone','mode','off')
    return 1

#解锁指令
def UnlockFlight():
    global uav
    pod = Fight.Flight_Action()
    data =pod.Unlock()
    uav.Send(data)
    r.hset(uav.id,'unlock','off')
    return 1

#起飞
def Takeoff():
    pod = Fight.Flight_Action()
    data =pod.Land()
    uav.Send(data) 
    r.hset(uav.id,'land','off')
    return 1

#返回
def ReturnBack():
    pod = Fight.Flight_Action()
    data =pod.Return()
    uav.Send(data)  
    r.hset(uav.id,'return','off')

#系统自检
def RunSelfCheck():
    global SelfCheck
    SelfCheck = 1
    #电池电压  (配置文件的电池电压参数)
    if SelfCheck == 1 :
        if uav.uavdata.v < 44:
            SelfCheck =0 
            consolelog("电压自检失败")
        else:
            SelfCheck =1
            consolelog("电压自检正常")

    
    # 定位状态
    if SelfCheck == 1 :
        if uav.uavdata.offset_staus == 0:
            SelfCheck =0 
            consolelog("定位自检失败")
        else:
            SelfCheck = 1
            consolelog("定位自检正常")

    # 丢星时间
    if SelfCheck == 1 :
        if uav.uavdata.gps_lost > 0:
            SelfCheck =0 
            consolelog("丢星时间自检失败")
        else:
            SelfCheck = 1
            consolelog("丢星正常")

    # 俯仰角
    if SelfCheck == 1 :
        if uav.uavdata.pitch/100 > 3:
            SelfCheck =0 
            consolelog("俯仰角自检失败")
        else:
            SelfCheck = 1
            consolelog("俯仰角自检正常")

    # 横滚角
    if SelfCheck == 1 :
        # consolelog(uav.uavdata.roll_angle)
        if uav.uavdata.roll_angle/100 > 3:
            SelfCheck =0 
            consolelog("横滚角自检失败")
        else:
            SelfCheck = 1
            consolelog("横滚角自检正常")

    # 磁罗盘连接 无人机遥测信息第71-72字节第二位是不是1 不是1则异常
    if SelfCheck == 1 :
        if uav.mc != 1:
            SelfCheck =0 
            consolelog("磁罗盘连接自检失败")
        else:
            SelfCheck = 1
            consolelog("磁罗连接正常")

    # 磁罗盘测向和卫星测向偏差
    if SelfCheck == 1:
        pod = Fight.Flight_Action()
        data =pod.MagneticDeclination()
        uav.Send(data) 
        data =pod.Double_Antenna_Off()
        uav.Send(data)
        magnetic_declination = uav.uavdata.toward_angle/10
        data =pod.Double_Antenna_On()
        uav.Send(data)
        direction = uav.uavdata.toward_angle/10
        if abs(magnetic_declination - direction) > 3 :
            SelfCheck = 0 
            consolelog("测向自检失败")
        else:
            SelfCheck = 1
            consolelog("测向自检正常")
            

    # 舱盖状态
    if SelfCheck == 1 :
        if airport.airportdata.warehouse_status != 0: 
            SelfCheck =0 
            consolelog("舱盖自检失败")
        else:
            SelfCheck = 1
            consolelog("舱盖自检正常")

    # 归机机构状态
    if SelfCheck == 1 :
        if airport.airportdata.homing_status != 0: 
            SelfCheck =0 
            consolelog("归机机构自检失败")
        else:
            SelfCheck = 1
            consolelog("归位自检正常")

    # 自检完成  
    if SelfCheck == 1:
        consolelog("自检完成")
        msg_dict ={'type':'selfchecksuccess'}
        msg = json.dumps(msg_dict)
        mqttclient.publish(TOPIC_INFO, msg)
        r.hset(uav.id,'check','off')
                
#开仓门
def OpenAirport():
    pod = Fight.Hatch_control()
    data =pod.OpenHatch()
    airport.Send(data) 
    r.hset(uav.id,'hatch','off')
    return 1

#关仓门
def CloseAirport():
    pod = Fight.Hatch_control()
    data =pod.CloseHatch()
    airport.Send(data) 
    r.hset(uav.id,'hatch','on')
    return 1

#
def UnlockAirport():
    pod = Fight.Hatch_control()
    data =pod.UnlockHatch()
    airport.Send(data) 

    return 1

#开仓门
def LockAirport():
    pod = Fight.Hatch_control()
    data =pod.LockHatch()
    airport.Send(data) 

    return 1

#发送航线
def send_path(path):
    #发送航线数据
    global flightPath
    if not isinstance(path, list):
        path = json.loads(path)
    # len(path)
    #add last path 
    last_point ={'coord':[uav.lon,uav.lat,uav.height],'speed': path[0]['speed'],'hovertime':path[0]['hovertime'],
    'radius':path[0]['radius'],'photo':path[0]['photo'],'heightmode':path[0]['heightmode'],'turning':path[0]['turning']}
    path.append(last_point)

    # global flight_json_road
    # flight_json_road =path
    r.hset(uav.id,'current_fly',json.dumps(path))

    uav.comfirmIndex=1
    # flightPath =copy.deepcopy(path)
    pod = Fight.Flight_Course_Struct()
    # consolelog("path "+path[0])
    data =pod.PathUpdate(path[0]['coord'][0],path[0]['coord'][1],path[0]['coord'][2],path[0]['speed'],path[0]['hovertime'],path[0]['radius'],path[0]['photo'],path[0]['heightmode'],path[0]['turning'],len(path),1)

    uav.Send(data) 
    
    flightPath.clear()
    #save senddata
    flightPath.append(data)

    length = len(path)
    # consolelog('航线 点'+str(length))
    uav.lastIndex =1
    uav.nextIndex =1
    uav.flightLength =length
    uav.path_loaded = False
    
    consolelog("->第 1 / %d 个点 %.7f %.7f %f"%(length,path[0]['coord'][0],path[0]['coord'][1],path[0]['coord'][2]))
    trytimes =0
    time.sleep(1)
    while uav.lastIndex < length  and trytimes <10 :
        # try:
            # uav.nextIndex = Fight.Course_Confirm.next

            print('航线 next '+ str(uav.lastIndex ) + ' ' +str(uav.nextIndex))
            if uav.lastIndex == uav.nextIndex :
                
                data =pod.PathUpdate(path[uav.nextIndex-1]['coord'][0],path[uav.nextIndex-1]['coord'][1],path[uav.nextIndex-1]['coord'][2],
                                    path[uav.nextIndex-1]['speed'],path[uav.nextIndex-1]['hovertime'],path[uav.nextIndex-1]['radius'],
                                    path[uav.nextIndex-1]['photo'],path[uav.nextIndex-1]['heightmode'],path[uav.nextIndex-1]['turning'],len(path),uav.nextIndex)
                uav.Send(data)
                trytimes =0
                # print("repeat",data.hex())
                

            if uav.lastIndex+1 == uav.nextIndex:
                uav.lastIndex = uav.nextIndex
                trytimes =0
                
                data =pod.PathUpdate(path[uav.nextIndex-1]['coord'][0],path[uav.nextIndex-1]['coord'][1],path[uav.nextIndex-1]['coord'][2],
                                    path[uav.nextIndex-1]['speed'],path[uav.nextIndex-1]['hovertime'],path[uav.nextIndex-1]['radius'],
                                    path[uav.nextIndex-1]['photo'],path[uav.nextIndex-1]['heightmode'],path[uav.nextIndex-1]['turning'],len(path),uav.nextIndex)
                uav.Send(data)
                flightPath.append(data)
                
                # if uav.nextIndex-1 < len(path):
                #     consolelog("->第 %d 个点 %.7f %.7f %f"%(uav.nextIndex,path[uav.nextIndex-1]['coord'][uav.nextIndex-1],path[uav.nextIndex-1]['coord'][1],path[uav.nextIndex-1]['coord'][2]))
                # print(uav.nextIndex + "path" +len(path))
                consolelog("->第 %d / %d个点 %.7f %.7f %f"%(uav.nextIndex,length,path[uav.nextIndex-1]['coord'][0],path[uav.nextIndex-1]['coord'][1],path[uav.nextIndex-1]['coord'][2]))
            time.sleep(1)
            trytimes +=1
            # if(trytimes >5):
            #     uav.nextIndex +=1
        # except KeyboardInterrupt:
        #     print("exit....")
        #     return 0
        #     break
    waittime =10
    while uav.path_loaded ==False and waittime >0:
        waittime -=1
        time.sleep(1)
    if(uav.path_loaded ==False):
        return 1
    print("do send ....",trytimes)
    return 0


#回放数据
def replay(history):
    global uavreplay
    # if isReplay == 1:
    #     return
    # if uavreplay is globals() : 
    #     uavreplay.isStop=True
    uavreplay = UavReplayThread(history)
    uavreplay.start()
    
    # msg_dict ={'cmd':'replay','history_id': history}
    # msg = json.dumps(msg_dict)
    # mqttclient.publish(FLY_CTRL, msg)
    consolelog("回放数据")
     
def stop():
    global uavreplay
    if isset('uavreplay') == 1:
        uavreplay.Stop()
        


def pause():
    global uavreplay
    if isset('uavreplay') == 1:
        uavreplay.isPause = True

def next():
    global uavreplay
    if isset('uavreplay') == 1:
        uavreplay.isPause = False

def seek(pos):

    global uavreplay
    if isset('uavreplay') == 1:
        uavreplay.seek = pos

    
#系统各种按钮当前状态
def send_state():
    # HIS = HistoryID
    planid =r.get('plan')
    if(planid == None):
        planid = -1
    historyid = r.hget(uav.id, 'historyid') 
    if(historyid == None):
        historyid = -1
    
    msg_dict ={
        'drone': {  
            "check": { "data": r.hget(uav.id, 'check') .decode()},
            "unlock": { "data": r.hget(uav.id, 'unlock') .decode()},         
            "lock": { "data": r.hget(uav.id, 'lock') .decode()},
            "takeoff": { "data": r.hget(uav.id, 'takeoff') .decode()},
            "return": { "data": r.hget(uav.id, 'return') .decode()},
            "land": { "data": r.hget(uav.id, 'land') .decode()},
            "light": { "data": r.hget(uav.id, 'light') .decode()},
            "mode": { "data": r.hget(uav.id, 'mode') .decode()},
            "historyid": { "data": int(historyid)},
            "planid": { "data": int( planid.decode())},
        },
        'monitor': { 
            "video": { "data": r.hget(uav.id, 'video') .decode()},
            "photo": { "data": r.hget(uav.id, 'photo') .decode()},
            "positioning": { "data": r.hget(uav.id, 'positioning') .decode()}
        },
        'hangar':{ 
            "hatch": { "data": r.hget(uav.id, 'hatch') .decode()},
            "charging": { "data": r.hget(uav.id, 'charging') .decode()},
            "mechanism": { "data": r.hget(uav.id, 'mechanism') .decode()},
            "wind_angle": { "data": r.hget(uav.id, 'wind_angle') .decode()},
            "rain_snow": { "data": r.hget(uav.id, 'rain_snow') .decode()},
            "out_temp": { "data": r.hget(uav.id, 'out_temp') .decode()},
            "in_temp": { "data": r.hget(uav.id, 'in_temp') .decode()},
        },
        'player':{ 
            "play": { "data":int(historyid)},
            "pause": { "data": r.hget(uav.id, 'pause') .decode()},
            "speed": { "data":  r.hget(uav.id, 'speed') .decode()}
        }
    }
    # consolelog("-----send ",msg_dict) 
    msg = json.dumps(msg_dict)
    mqttclient.publish(TOPIC_STATE, msg)

#最后50个点 经纬度，和高度


#发送巡检路径
def send_json_path():
    flight_json_road =r.hget(uav.id,'current_fly')

    if flight_json_road is  None:
        return
    #没有无人机
    if isset('uav') == 0:
        return
    
    #无人机没数据
    this_time = time.time()
    if uav.updateTime < this_time -100:
        return
        

    jsondata = json.loads(flight_json_road)

    msg_dict ={
        'road':jsondata
    }
    msg = json.dumps(msg_dict)
    mqttclient.publish(TOPIC_STATE, msg)

#故障中断
def clean_json_path():
    r.delete('current_fly')
    msg_dict ={
        'break':'on'
    }
    msg = json.dumps(msg_dict)
    mqttclient.publish(TOPIC_STATE, msg)
    
#清空巡检路径
def clean_json_path():
    r.delete('current_fly')
    msg_dict ={
        'break':'on'
    }
    msg = json.dumps(msg_dict)
    mqttclient.publish(TOPIC_STATE, msg)
    
#定点巡航
def send_pointpath(point):
    pod = Fight.Course_Set_Struct()
    data =pod.point(point['coord'][0],point['coord'][1],point['coord'][2],point["radius"],point['time'],point['direction'],point['mode'],point['speed'])
    uav.Send(data)    
    # consolelog('send pointpath successed')


async def on_message(client, topic, payload, qos, properties):
    # print(f'RECV MSG: {topic} {payload}')
    # try:
    jsondata = json.loads(payload)
    
    # result = cmp(jsondata['cmd'], 'snapshot')
    cmd = jsondata['cmd']
    param = None
    if 'data' in jsondata:
        param = jsondata['data']

    if topic ==FLY_CTRL:
        #启动回放
        if  cmd =='player/play':
            history_id = jsondata['history_id']
            replay(history_id)
            consolelog("启动回放")
            r.hset(uav.id,'HistoryID',history_id)
            
        global SelfCheck
        #退出回放
        if  cmd =='player/stop':
            replayid = r.hget(uav.id,'HistoryID')
            replayid = int(replayid)
            if(replayid > 0 ):
                consolelog("退出回放")
                stop()

        #暂停回放
        if  cmd =='player/pause' and param == 'on':
            consolelog("暂停")
            pause()
            r.hset(uav.id,'pause','off')

        #继续回放
        elif  cmd =='player/pause'and param == 'off':
            consolelog("继续回放")
            next()
            r.hset(uav.id,'pause','on')
        

        #调整播放倍速
        elif  cmd == 'player/speed':
            if uavreplay is not None:
                uavreplay.speed=(1/param)
            r.hset(uav.id,'speed',param)

        #播放位置调整
        elif  cmd =='player/seek':
            seek(param)
        send_state()
        return
        

    if topic ==TOPIC_CTRL:
        #系统状态
        
        if  cmd =='dofly':
            consolelog("准备启动")
            if(isset('auto') and auto.is_alive()):
                consolelog("有正在执行的巡航任务")
                return
            history_id = jsondata['historyid']
            path = jsondata['data']
            consolelog("准备巡航")
            auto = AutoThread(path,history_id)
            auto.start()
            
            if not os.path.exists("./history"):
                os.mkdir('./history',755)
            if(history_id):
               uav.history_id = history_id
            # await(go_fly(param,history))


        elif  cmd =='fly_over':
            uav.history_id = -1
            
            if(isset('auto') and auto.is_alive()):
                auto.Stop()
            
        #系统状态
        elif  cmd =='state':
            send_state()
            
        #获取路径
        elif  cmd =='road':
            consolelog("读取路线")
            send_json_path()



        #航线指令##
        elif  cmd =='drone/plan':
            # circle = param path id
            if(uav.test_freq == 0):
                consolelog("无人机未连接")
                return
            planid =r.get('plan')

            if planid is not None and int(param) == int(planid):
               return
            msg_dict ={"cmd":"corn"}
            msg = json.dumps(msg_dict)
            mqttclient.publish(FLY_CTRL, msg)
            r.set('plan',param)
            if int(param) == -1:
                consolelog("停止巡检")
            else:
                consolelog("创建巡检计划 "+str(param))
            send_state()
            return

        #航线加载
        elif  cmd =='drone/route':
            # if(isset('auto') and auto.is_alive()):
            #     return
            # history_id = jsondata['historyid']
            # path = jsondata['data']
            # consolelog("准备巡航")
            # print(" param  " + str(param)
            # auto = AutoThread(path)
            # auto.start()
                  
            send_path(param)

        #航线圈数
        elif  cmd =='drone/circle':
            # circle = param
            pod = Fight.Flight_Circle_Struct()
            data =pod.turns(param)
            uav.Send(data)

        #定点巡航
        elif  cmd =='drone/point':
            send_pointpath(param)

        ##无人机指令##
        
        elif  cmd == 'drone/check':
            consolelog("自检开始")
            RunSelfCheck()
        
        ##机场指令##
        elif cmd == 'hangar/hatch'and param =='on':
            pod = Fight.Hatch_control()
            data =pod.OpenHatch()
            airport.Send(data) 
            r.hset(uav.id,'hatch','off')
            


        elif cmd == 'hangar/hatch'and param =='off':
            pod = Fight.Hatch_control()
            data =pod.CloseHatch()
            airport.Send(data) 
            r.hset(uav.id,'hatch','on')
            

        #归位锁定   
        elif cmd == 'hangar/mechanism'and param =='on':
            pod = Fight.Homing_control()
            data =pod.HomeLock()
            airport.Send(data) 
            r.hset(uav.id,'mechanism','off')
            

        #归位解锁
        elif cmd == 'hangar/mechanism'and param =='off':
            pod = Fight.Homing_control()
            data =pod.HomeUnlock()
            airport.Send(data) 
            r.hset(uav.id,'mechanism','on')
            
    

        elif cmd == 'hangar/charging'and param =='on':
            pod = Fight.Charge_control()
            data =pod.Charge()
            airport.Send(data) 
            r.hset(uav.id,'charging','off')
            


        elif cmd == 'hangar/charging'and param =='off':
            pod = Fight.Charge_control()
            data =pod.ChargeOff()
            airport.Send(data) 
            r.hset(uav.id,'charging','on')
            
        ##载荷指令##
        elif cmd == 'monitor/up':
            pod = Fight.Pod_Send()
            data =pod.FieldUp()
            cam.Send(data) 
            hearbeatthread.camData=1
            return

        elif cmd == 'monitor/down':
            pod = Fight.Pod_Send()
            data =pod.FieldDown()
            cam.Send(data)
            hearbeatthread.camData=1
            return

        elif cmd == 'monitor/left':
            pod = Fight.Pod_Send()
            data =pod.FieldLeft()
            cam.Send(data)     
            hearbeatthread.camData=1
            return

        elif cmd == 'monitor/right':
            pod = Fight.Pod_Send()
            data =pod.FieldRight()
            cam.Send(data) 
            hearbeatthread.camData=1
            return

        elif cmd == 'monitor/centering':
            pod = Fight.Pod_Send()
            data =pod.Centering()
            # consolelog(data.hex())
            cam.Send(data)   
            r.hset(uav.id,'centering','off') 
             
        
        elif cmd == 'monitor/photo':
            pod = Fight.Pod_Send()
            data =pod.Photo()
            cam.Send(data) 
            r.hset(uav.id,'photo','off') 
            

        elif cmd == 'monitor/video' and param =='on':
            pod = Fight.Pod_Send()
            data =pod.Video()
            cam.Send(data) 
            r.hset(uav.id,'video','off')
             

        elif cmd == 'monitor/video' and param =='off':
            pod = Fight.Pod_Send()
            data =pod.Video()
            cam.Send(data) 
            r.hset(uav.id,'video','on') 
             

        elif cmd == 'monitor/view+':
            pod = Fight.Pod_Send()
            data =pod.LargenField()
            cam.Send(data)
            hearbeatthread.camData=1
            return

        elif cmd == 'monitor/view-':
            pod = Fight.Pod_Send()
            data =pod.ReduceField()
            cam.Send(data) 
            hearbeatthread.camData=1
            return

        elif cmd == 'monitor/focus+':
            pod = Fight.Pod_Send()
            data =pod.FocusUp()
            cam.Send(data) 
            hearbeatthread.camData=1
            return

        elif cmd == 'monitor/focus-':
            pod = Fight.Pod_Send()
            data =pod.FocusDown()
            cam.Send(data) 
            hearbeatthread.camData=1
            return
        
        #stop view/focus
        elif cmd == 'monitor/stop':
            pod = Fight.Pod_Send()
            data =pod.Stop()
            cam.Send(data)
            hearbeatthread.camData=None
            

        elif cmd == 'monitor/positioning'and param =='on':
            pod = Fight.Pod_Send()
            data =pod.OpenLaser(uav.uavdata.pitch,uav.uavdata.roll_angle,uav.uavdata.toward_angle,uav.uavdata.lon,uav.uavdata.lat,uav.uavdata.height,uav.uavdata.rel_height)
            cam.Send(data) 
            r.hset(uav.id,'positioning','off')

        elif cmd == 'monitor/positioning'and param =='off':
            pod = Fight.Pod_Send()
            data =pod.CloseLaser(uav.uavdata.pitch,uav.uavdata.roll_angle,uav.uavdata.toward_angle,uav.uavdata.lon,uav.uavdata.lat,uav.uavdata.height,uav.uavdata.rel_height)
            cam.Send(data) 
            r.hset(uav.id,'positioning','on')
            

        elif cmd == 'monitor/tracking':
            pod = Fight.Pod_Send()
            data =pod.Tracking(uav.uavdata.pitch,uav.uavdata.roll_angle,uav.uavdata.toward_angle,uav.uavdata.lon,uav.uavdata.lat,uav.uavdata.height,uav.uavdata.rel_height)
            cam.Send(data) 
            r.hset(uav.id,'tracking','off')
            

        elif cmd == 'monitor/collect':
            pod = Fight.Pod_Send()
            data =pod.Collect()
            cam.Send(data) 
            r.hset(uav.id,'collect','off')
            

        elif cmd == 'monitor/downward':
            pod = Fight.Pod_Send()
            data =pod.Downward()
            cam.Send(data) 
            r.hset(uav.id,'downward','off')
            

        elif cmd == 'monitor/scanning':
            pod = Fight.Pod_Send()
            data =pod.Scanning()
            cam.Send(data) 
            r.hset(uav.id,'scanning','off')
            

        elif cmd == 'monitor/imageswitch':
            pod = Fight.Pod_Send()
            data =pod.ImageSwitch()
            cam.Send(data) 
            r.hset(uav.id,'imageswitch','off')
            
            

        if SelfCheck == 1:
            if cmd == 'drone/unlock' :
                pod = Fight.Flight_Action()
                data =pod.Unlock()
                uav.Send(data)
                r.hset(uav.id,'unlock','off')

            elif cmd == 'drone/takeoff':
                pod = Fight.Flight_Action()
                data =pod.TakeOff()
                uav.Send(data)
                r.hset(uav.id,'takeoff','off')

            elif cmd == 'drone/lock':
                pod = Fight.Flight_Action()
                data =pod.Lock()
                uav.Send(data) 
                r.hset(uav.id,'lock','on')
                #lock 
                r.hset(uav.id,'takeoff','on')
                r.hset(uav.id,'check','on')
                r.hset(uav.id,'unlock','on')
                r.hset(uav.id,'land','on')
                r.hset(uav.id,'takeoff','on')
                r.hset(uav.id,'return','on')
                r.hset(uav.id,'light','on')
                
                

            elif cmd == 'drone/mode' and param =='automatic':
                pod = Fight.Flight_Action()
                data =pod.AutomaticControl()
                consolelog("自动控制")
                uav.Send(data)  
                r.hset(uav.id,'mode','off')

            elif cmd == 'drone/mode' and param =='manual':
                pod = Fight.Flight_Action()
                data =pod.ManualControl()
                consolelog("手动控制")
                uav.Send(data) 
                r.hset(uav.id,'mode','on')

            elif cmd == 'drone/return':
                pod = Fight.Flight_Action()
                data =pod.Return()
                uav.Send(data)  
                consolelog("飞机返程")
                r.hset(uav.id,'return','off')

            elif cmd == 'drone/land':
                pod = Fight.Flight_Action()
                data =pod.Land()
                uav.Send(data) 
                consolelog("飞机降落")
                r.hset(uav.id,'land','off')

            elif cmd == 'drone/light' and param =='on':
                pod = Fight.Flight_Action()
                data =pod.Anticollision_Light_On()
                uav.Send(data) 
                consolelog("防撞灯开")
                r.hset(uav.id,'light','off')

            elif cmd == 'drone/light' and param =='off':
                pod = Fight.Flight_Action()
                data =pod.Anticollision_Light_Off()
                uav.Send(data)
                consolelog("防撞关")
                r.hset(uav.id,'light','on')
                
            elif cmd == 'drone/controller' and param =='on':
                pod = Fight.Flight_Action()
                data =pod.Controller_On()
                uav.Send(data)  

            elif cmd == 'drone/controller' and param =='off':
                pod = Fight.Flight_Action()
                data =pod.Controller_Off()
                uav.Send(data)         

            elif cmd == 'drone/double antenna' and param =='on':
                pod = Fight.Flight_Action()
                data =pod.Double_Antenna_On()
                uav.Send(data)     

            elif cmd == 'drone/double antenna' and param =='off':
                pod = Fight.Flight_Action()
                data =pod.Double_Antenna_Off()
                uav.Send(data)  

            elif cmd == 'drone/magnetic declination' and param =='on':
                pod = Fight.Flight_Action()
                data =pod.MagneticDeclination()
                uav.Send(data)     

        send_state()
        # else:
        #     consolelog("自检未完成")


    
def on_connect(client, flags, rc, properties):
    print('mqtt Connected')

def on_subscribe(client, mid, qos, properties):
    print('mqtt SUBSCRIBED')

def on_disconnect(client, packet, exc=None):
    print('mqtt Disconnected')

def ask_exit(*args):
    STOP.set()

async def mqttconnect(broker_host):
    global mqttclient
    mqttclient = MQTTClient("client-id222"+str(random.random()))

    mqttclient.on_connect = on_connect
    mqttclient.on_message = on_message
    mqttclient.on_subscribe = on_subscribe
    mqttclient.on_disconnect = on_disconnect

    # Connectting the MQTT brokewarehouser
    await mqttclient.connect(broker_host)

    # Subscribe to topic
    mqttclient.subscribe(TOPIC_CTRL)
    mqttclient.subscribe(FLY_CTRL)
    # Send the data of test
    # mqttclient.publish("TEST/A", 'AAA')
    # mqttclient.publish("TEST/A", 'BBB')

    # await STOP.wait()
    # await mqttclient.disconnect()


#心跳线程
class HearbeatThread(threading.Thread):
    def __init__(self):
        super(HearbeatThread,self).__init__()

        self.uav_time = time.time()
        self.cam_time = time.time()
        self.airport_time = time.time()
        self.uav_num = 0
        self.cam_num = 0
        self.isStop =False
        self.isStart=False
        self.camData =None

    def Stop(self):
        self.isStop = True

    def Next(self):
        self.isStop = False

    def run(self):
        hb = Fight.Flight_HeartBeat()
        pod_hb = Fight.Pod_Send()
        # print("111")
        while self.isStop == False:           
            current=time.time()
            if(current > uav.updateTime+60 or current > cam.updateTime+60 ):
                msg_dict ={'cmd':'start_uav'}
                msg = json.dumps(msg_dict)
                mqttclient.publish(FLY_CTRL, msg)
                return

            if self.uav_time +1 < current and uav is not None:
                global IsMaster
                IsMaster = 1
                data = hb.SendHeartBeat()
                uav.Send(data)
                self.uav_time=current
                # self.uav_num += 1 
                # print("已发送heartbeat次数:",self.uav_num)

            if isset('cam') ==1  and self.cam_time + 0.2< current and self.camData is None :
                
                data = pod_hb.Cambeat(uav.uavdata.pitch,uav.uavdata.roll_angle,uav.uavdata.toward_angle,uav.uavdata.lon,uav.uavdata.lat,
                                      uav.uavdata.height,uav.uavdata.rel_height,uav.uavdata.gps_stars)
                cam.Send(data)
                self.cam_time =current
                # self.cam_num += 1 
                # print("已发送cambeat次数:",self.cam_num)



# #摇杆线程
class JoystickThread(threading.Thread):
    def __init__(self,tty):
        super(HearbeatThread,self).__init__()
        self.ser = serial.Serial(tty.strip(), 115200)   # 'COM1'为串口名称，根据实际情况修改；9600为波特率，也可以根据设备要求调整
        self.isStop =False
        self.data = Fight.COM_JoyStick()


    def Stop(self):
        self.isStop = True

    def Next(self):
        self.isStop = False

    def run(self):
        while self.isStop == False:           
            data  = self.ser.read(size=32)
            ctypes.memmove(ctypes.addressof(self.data), data, ctypes.sizeof(self.airportdata))
            if self.data.head == 0xaa and self.data.head2 == 0xc8:
                print('com from '+self.data)


#无人机回放数据
class UavReplayThread(threading.Thread):
    def __init__(self ,history_id):
        super(UavReplayThread,self).__init__()
        self.history_id = history_id
        self.isStop =False
        self.isPause = False
        self.speed =1
        self.seek =-1
        self.f=None
        self.uavdata = Fight.Flight_Struct()

    def Stop(self):
        self.isStop = True
        self.isPause =True
        if self.f is not None:
            self.f.close()
        self.f = None

    def get_id(self): 
		# returns id of the respective thread 
        if hasattr(self, '_thread_id'): 
            return self._thread_id 
        for id, thread in threading._active.items(): 
            if thread is self: 
                return id
    def raise_exception(self): 

        thread_id = self.get_id() 
                #精髓就是这句话，给线程发过去一个exceptions，线程就那边响应完就停了
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 
        	ctypes.py_object(SystemExit)) 
        if res > 1: 
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0) 
            print('Exception raise failure') 

   
    def run(self):
        test=Fight.Flight_REPLAY_Struct()
        
        history_file = 'history/{}'.format(self.history_id)
        print("kaishi"+history_file)
        self.f =open(history_file, 'rb')
        self.f.seek(0, os.SEEK_END) 
        filelen = self.f.tell()
        self.f.seek(0, os.SEEK_SET) 
        a = int('a5',16)
        b = int('5a',16)
        cmd = int('10',16)
        # print("===len "+str(filelen))
        while self.isStop ==False:
            while self.isPause ==False:
                # print(self.isStop)
                if(self.seek>=0):
                    self.f.seek(int(filelen * self.seek))
                    self.seek = -1
                    
                data = self.f.read(1)
                currentpos = self.f.tell()
                # print("==="+str(currentpos) +" / "+str(filelen))
                #播放结束
                if currentpos >= filelen:
                    self.isStop=True
                    self.raise_exception()
                    break
              
                
                head = struct.unpack("B", data)
                # print("=0x%x "%(head))
                if a == int.from_bytes(head, byteorder='little'):
                    # print("=0x%x "%(head))
                    data = self.f.read(1)
                    head2 = struct.unpack("B", data)
                    if b == int.from_bytes(head2, byteorder='little'):
                        # print("---->0x%x"%(head2))

                        #lenght
                        lenc = self.f.read(1)
                        len2 = struct.unpack("B", lenc)
                        len = int.from_bytes(len2, byteorder='little')

                        datacmd = self.f.read(1)
                        rcmd = struct.unpack("B", datacmd)
                        #left length
                        if  cmd == int.from_bytes(rcmd, byteorder='little') and len == 128:
                            
                            left = len -4
                            data = self.f.read(left)
                            
                            databuffer =b''
                            databuffer = lenc +datacmd + data
                            todata=bytes(bytearray(databuffer))
                            ctypes.memmove(ctypes.addressof(test), todata, ctypes.sizeof(test))
                            truee = test.CheckCRC(todata,test.crc)
                            if not truee:
                                continue
                     

                            msg_dict ={'type':'drone','data': {
                                'temp':test.temp,
                                'eng':test.eng,
                                'v':test.v/10,
                                'a':test.a/10,
                                'offset_staus':test.offset_staus,
                                'speed':test.speed/100,
                                'lat': test.lat/10000000,  #纬度
                                'lon': test.lon/pow(10,7),  #经度
                                'height': test.height,   #高度
                                'rel_height':test.rel_height/10,   
                                'real_height':test.real_height/100,
                                'target_speed':test.target_speed/100,
                                'speed':test.speed/100,   #地速x100
                                'gps_speed':test.gps_speed/100, 
                                'trajectory':test.trajectory/10,  #gui ji  jiao
                                'pitch':test.pitch /100,     #俯仰角
                                'roll_angle':test.roll_angle/100,  #滚转角
                                'fu_wing':test.fu_wing /100,
                                'updown':test.updown/100,
                                'speedup':test.speedup/100,
                                'toward':test.toward/100,    #航向角
                                'lock':test.lock,
                                'toward_angle':test.toward_angle/10,
                                'fly_ctl':test.fly_ctl,
                                'staus':test.staus,
                                'fly_status':test.fly_status,
                                'gps_lost':test.gps_lost,
                                'link_lost':test.link_lost,
                                'area':test.area,
                                'turns_done':test.turns_done,
                                'turns_todo':test.turns_todo,
                                'fly_distance':test.fly_distance,
                                'fly_time':test.fly_time,
                                'target_point':test.target_point,
                                'target_height':test.target_height/10,
                                'target_angle':test.target_angle/10,
                                'stay_time':test.stay_time,
                                'flyctl_v':test.flyctl_v/10,
                                'engine_v':test.engine_v/10,
                                'gps_stars':test.gps_stars,
                                'year':test.year,
                                'month':test.month,
                                'day':test.day,
                                'hour':test.hour,
                                'min':test.min,
                                'sec':test.sec,
                                'flyctl_temp':test.flyctl_temp,
                                'offset_dist':test.offset_dist,
                                'HDOP':test.HDOP,
                                'VDOP':test.VDOP,
                                'SDOP':test.SDOP,
                                'height_cm':test.height_cm,
                                'postion':float(currentpos)/float(filelen),
                                
                                }
                            }
                            

                            msg = json.dumps(msg_dict)
                            # print("playback ---->\n")
                
                            mqttclient.publish(TOPIC_INFO, msg)
                            time.sleep(self.speed)

            
#无人机处理线程
class UavThread(threading.Thread):
    def __init__(self ,id,recvport,targetip,targetport,iszubo):
        super(UavThread,self).__init__()
        self.id = "uav_"+id
        self.lon =114.345317
        self.lat =38.0977876
        self.freq =0
        self.test_freq=0
        self.height=104

        r.set('uav',self.id) 
        r.hset(self.id,'lat', self.lat)
        r.hset(self.id,'lon', self.lon)
        r.hset(self.id,'height',self.height)

        #接受无人机端口
        if( iszubo == "1"):
            self.zubo_init(targetip,targetport,recvport)
        else:
            self.dan_init(targetip,targetport,recvport)
        self.doFlyFile =None
        self.uavdata = Fight.Flight_Struct()
        self.locate=0.0
        self.mc=0.0
        self.v=0.0
        self.startTime = 0
        self.nextIndex=0
        self.lastIndex=0
        self.HeartbeatCheck = 0
        self.flightLength =0
        self.comfirmIndex =0
        self.mqttclient =None
        self.history_id = -1
        self.fps = 0
        self.iszubo = iszubo == "1"

        self.path_loaded = False
        


     
        #无人机 目标地址和端口
        self.uav_addr = (targetip, targetport)

        self.updateTime =time.time()
        
    
        #status init   
        r.hset(self.id, 'check','on') 
        r.hset(self.id, 'unlock','on')
        r.hset(self.id, 'lock','on') 
        r.hset(self.id, 'takeoff','on') 
        r.hset(self.id, 'return','on') 
        r.hset(self.id, 'land','on') 
        r.hset(self.id, 'light','on')
        r.hset(self.id, 'mode','on')
        r.hset(self.id, 'historyid',-1)
        r.hset(self.id, 'video','on') 
        r.hset(self.id, 'photo','on')
        r.hset(self.id, 'positioning','on')
        r.hset(self.id, 'hatch','on')
        r.hset(self.id, 'charging','on') 
        r.hset(self.id, 'wind_angle',0)
        r.hset(self.id, 'rain_snow',0)
        r.hset(self.id, 'out_temp',0)
        r.hset(self.id, 'in_temp',0)
        r.hset(self.id, 'mechanism','on')
        r.hset(self.id, 'pause','on') 
        r.hset(self.id, 'speed','on')

        # pod = Fight.Flight_Action()
        # data =pod.Unlock()
        # self.Send(message)
    def zubo_init(self,ip ,port,rport):
        routeadd = "sudo route add -net "+ip+" netmask 255.255.255.255 dev "+eth
        # os.system(routeadd)
        cmdrun = 'echo %s | sudo -S %s' % (rootpassword, routeadd)
        print(cmdrun)
        os.system(cmdrun)

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 允许端口复用
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定本机IP和组播端口
        self.sock.bind(('', rport))
        # 设置UDP Socket的组播数据包的TTL（Time To Live）值
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        # 声明套接字为组播类型
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        # 加入多播组
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(ip) + socket.inet_aton('0.0.0.0'))
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 1024*1024*5)
        self.uav_udp_socket =self.sock
     


    def dan_init(self,ip ,port,rport):
        print(" dan init "+ip+" loacl port "+str(rport))
        uav_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        uav_recv_socket.bind(("", rport))
        self.sock = uav_recv_socket
           #发送无人机创建UDP套接字
        self.uav_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.uav_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        
    def run(self):
        heartbeat =Fight.Flight_HeartBeat()
        comfirm =Fight.Course_Confirm()
        path=Fight.Flight_Course_Struct()
        pathquery=Fight.Flight_Course_Query()
        check=Fight.Flight_Manage()
        startTime =time.time()
        # history_id = self.
        # print("self.HeartbeatCheck "
        databuffer =b''
        global uavreplay
       
        offset =0
        data =b''
        
        a = hex(0xa5)
        b = hex(0x5a)
        todata =None
        while True: 
            # databuffer =b''
            if self.iszubo:
                if(len(databuffer) == 0):
                    data, _ = self.sock.recvfrom(1024)      # buffer size is 4096 bytes
                    # print(" ：Received message  {}: {}".format(len(data), data))
                    if self.doFlyFile is not None:
                        self.doFlyFile.write(data)
                else:
                    data=bytes(bytearray(databuffer))

                offset =0
                index =-1
            
                cmdlen =0
                while offset < len(data):
                    byte =data[offset]
                    byte2 =0
                    if offset < len(data)-1:
                        byte2 = data[offset+1]

                    if hex(byte) == a and hex(byte2) == b:
                        index = offset
                        if offset < len(data)-2:
                            cmdlen = data[offset+2]
                        break
                    offset +=1
                
                if index == -1:
                    
                    # print(" bad message  {}: {}".format(databuffer.hex(), data.hex()))
                    databuffer =b''
                    continue
                    
            
                # if foundheader2 and len(databuffer) == 0:
                # print("  message  {}: {}".format(index, data.hex()))
                databuffer=data[index:]
                
                while(len(databuffer)< cmdlen):
                    data, _ = self.sock.recvfrom(1024)      # buffer size is 4096 bytes
                    databuffer+=data
                    if self.doFlyFile is not None:
                        self.doFlyFile.write(data)
                todata=bytes(bytearray(databuffer))
                # print(" ：Received message  {}: {}".format(len(todata), todata.hex()))
                databuffer=databuffer[3:]
                # todata,_ = self.sock.recvfrom(1024)
            else:
                todata,_ = self.sock.recvfrom(1024)
                if self.doFlyFile is not None:
                        self.doFlyFile.write(todata)
            
            # print("to offset"+str(offset))
            now = time.time()
            if now > self.updateTime+1:
                self.test_freq =self.freq
                self.freq = 0
                self.updateTime =time.time()
                # print ("ssss  "+str(self.test_freq ))
            else:
                self.freq +=1
                
                
            
            if self.doFlyFile is None and self.history_id != -1:
                filepath = './history/{}'.format(self.history_id)
                self.doFlyFile = open(filepath, 'wb')
                print("save file "+filepath)
                
            if self.history_id == -1 and self.doFlyFile is not None:
                self.doFlyFile.close()
                self.doFlyFile = None
                

            
            # if(len(todata) != 128):
                # print("to package {}: {}".format(len(todata), todata.hex()))

            ctypes.memmove(ctypes.addressof(heartbeat), todata, ctypes.sizeof(heartbeat))
            # print(" get cmd "+hex(heartbeat.cmd)+ "  "+hex(heartbeat.s_cmd))

            if(heartbeat.cmd == 0x08):
                print(" get heart beat ")
                # self.HeartbeatCheck =1
                # databuffer = databuffer[heartbeat.length:]
            elif(heartbeat.cmd == 0x05 and heartbeat.s_cmd == 0x22):
                # consolelog("update route")
                ctypes.memmove(ctypes.addressof(comfirm), todata, ctypes.sizeof(comfirm))
                # self.nextIndex  = struct.unpack('<H',data[5:7])
                self.nextIndex  =  comfirm.next
                # print("path comfirm",databuffer.hex())
                print("update route index ",comfirm.next)
                # databuffer = databuffer[comfirm.length:]

                if self.nextIndex ==  self.flightLength +1:
                    print('-------------航线上传完成--------------')
                    consolelog("航线上传完成")
                    msg_dict ={'type':'loadsuccess'}
                    msg = json.dumps(msg_dict)
                    mqttclient.publish(TOPIC_INFO, msg)
                    code =check.Check()
                    uav.Send(code)
                 
            
            elif(heartbeat.cmd == 0x05 and heartbeat.s_cmd == 0x41):
                ctypes.memmove(ctypes.addressof(pathquery), todata, ctypes.sizeof(pathquery))
                print("-----------------------------------recieve query",pathquery.index)
                # print("check",data.hex())
                # print(data[6:24].hex())
                # print(flightPath[pathquery.index-1][6:24].hex())
                try:
                    # databuffer = databuffer[pathquery.length:]
                    if pathquery.index <= self.flightLength:
                        if todata[6:24] == flightPath[pathquery.index-1][6:24]  and todata[28:30] == flightPath[pathquery.index-1][28:30]:
                            code =comfirm.PointComfirm(self.flightLength,pathquery.index)
                            uav.Send(code)
                            if(pathquery.index == uav.comfirmIndex):
                                consolelog("检查第 %d 个点 %.7f %.7f %.2f"%(pathquery.index ,pathquery.lon/pow(10,7),pathquery.lat/pow(10,7),pathquery.height/1000))
                                uav.comfirmIndex +=1
                            
                            # consolelog("check send",code.hex())
                            if pathquery.index == self.flightLength:
                                print("-------------航线装订成功--------------")
                                send_json_path()
                                self.path_loaded = True
                        else:
                            consolelog("第 %d 个点不一致"%pathquery.index)

                        
                except:
                    print("Uav GET PATH Error!!!\n ")
                    
                # oldPath =path.PathUpdate(flightPath[pathquery.index]['coord'][0],flightPath[pathquery.index]['coord'][1],flightPath[pathquery.index]['coord'][2],flightPath[pathquery.index]['speed'],flightPath[pathquery.index]['hovertime'],flightPath[pathquery.index]['radius'],
                #             flightPath[pathquery.index]['photo'],flightPath[pathquery.index]['heightmode'],flightPath[pathquery.index]['turning'],len(flightPath),pathquery.index)
                # if np.all(oldPath,pathquery):
                #     code =pathquery.PathQuery(self.flightLength,pathquery.index+1)
                #     uav.Send(code)
                #     print("check send",code.hex())
                # else:
                #     print("check failure")

                # if pathquery.index == self.flightLength:
                #     print("check successful")
                
            elif(heartbeat.cmd == 0x10 and heartbeat.s_cmd == 0x10):
                
                # if  heartbeat.s_cmd == 0x10:
                #     self.fps += 1
                #     if time.time() +1 > fpstime:
                #         fpstime = time.time()

                ctypes.memmove(ctypes.addressof(self.uavdata), todata, ctypes.sizeof(self.uavdata))
            
              
                    
                truee = self.uavdata.CheckCRC(todata,self.uavdata.crc)
                # databuffer = databuffer[heartbeat.length:]
                # print(todata.hex()+'----check is '+str(truee))

                if not truee:
                    continue
                if(self.uavdata.length != 128):
                    continue
              
                self.lat = round(self.uavdata.lat/pow(10,7),8)
                self.lon = round(self.uavdata.lon/pow(10,7),8)
                self.height = self.uavdata.height
                
                r.hset(uav.id,'lat', self.lat)
                r.hset(uav.id,'lon', self.lon)
                r.hset(uav.id,'height',self.height)
                
                if isset('uavreplay') == 1 and uavreplay.is_alive():
                    # print('is replaying not send current status')
                    continue
                
                if  startTime + 2 < time.time():
                    # print(data[0:15].hex() )
                  
                    # self.uavdata.CheckCRC(data,self.uavdata.crc)
                    # if self.uavdata.cmd_back1 != 0x00:
                    #     print(hex(self.uavdata.cmd_back1))
                    #     print(hex(self.uavdata.cmd_back2))
                    
                 
#如果在回访状态，无人机数据不显示。
                    # if isReplay ==1:
                    #     continue
                    # print(self.uavdata.v/10)
                    # print(self.uavdata.a/10)
                    msg_dict ={'type':'drone','data': {
                    'temp':self.uavdata.temp,
                    'eng':self.uavdata.eng,
                    'v':self.uavdata.v/10,
                    'a':self.uavdata.a/10,
                    'offset_staus':self.uavdata.offset_staus,
                    'speed':self.uavdata.speed/100,
                    'lat': round(self.uavdata.lat/pow(10,7),8),  #纬度
                    'lon': round(self.uavdata.lon/pow(10,7),8) , #经度
                    'height': self.uavdata.height,   #高度
                    'rel_height':self.uavdata.rel_height/10,   
                    'real_height':self.uavdata.real_height/100,
                    'target_speed':self.uavdata.target_speed/100,
                    'speed':self.uavdata.speed/100,   #地速x100
                    'gps_speed':self.uavdata.gps_speed/100, 
                    'trajectory':self.uavdata.trajectory/10,  #gui ji  jiao
                    'pitch':self.uavdata.pitch /100,     #俯仰角
                    'roll_angle':self.uavdata.roll_angle/100,  #滚转角
                    'fu_wing':self.uavdata.fu_wing /100,
                    'updown':self.uavdata.updown/100,
                    'speedup':self.uavdata.speedup/100,
                    'toward':self.uavdata.toward/100,    #航向角
                    'lock':self.uavdata.lock,
                    'toward_angle':self.uavdata.toward_angle/10,
                    'fly_ctl':self.uavdata.fly_ctl,
                    'staus':self.uavdata.staus,
                    'fly_status':self.uavdata.fly_status,
                    'gps_lost':self.uavdata.gps_lost,
                    'link_lost':self.uavdata.link_lost,
                    'area':self.uavdata.area,
                    'turns_done':self.uavdata.turns_done,
                    'turns_todo':self.uavdata.turns_todo,
                    'fly_distance':self.uavdata.fly_distance,
                    'fly_time':self.uavdata.fly_time,
                    'target_point':self.uavdata.target_point,
                    'target_height':self.uavdata.target_height/10,
                    'target_angle':self.uavdata.target_angle/10,
                    'stay_time':self.uavdata.stay_time,
                    'flyctl_v':self.uavdata.flyctl_v/10,
                    'engine_v':self.uavdata.engine_v/10,
                    'gps_stars':self.uavdata.gps_stars,
                    'year':self.uavdata.year,
                    'month':self.uavdata.month,
                    'day':self.uavdata.day,
                    'hour':self.uavdata.hour,
                    'min':self.uavdata.min,
                    'sec':self.uavdata.sec,
                    'flyctl_temp':self.uavdata.flyctl_temp,
                    'offset_dist':self.uavdata.offset_dist,
                    'HDOP':self.uavdata.HDOP/10,
                    'VDOP':self.uavdata.VDOP/10,
                    'SDOP':self.uavdata.SDOP/10,
                    'height_cm':self.uavdata.height_cm,
                    "freq":self.test_freq
                    }
                    }
                    msg = json.dumps(msg_dict)
                    
                    if uav.uavdata.staus &(1<<1):
                        self.mc = 1
                    else:
                        self.mc = 0
                    # print(self.mc)

                    # r.hset('drohearbeatthreadmps(msg_dict)
                    # print ('mqttclient ',mqttclient)
                    # print("uav --->:")
                    if isset("mqttclient") == 1:
                        mqttclient.publish(TOPIC_INFO, msg)

            # print(self.HeartbeatCheck)
            # if  (time.time()-self.startTime) >5 and self.HeartbeatCheck ==0:
            #     # print("3333")
            #     if not hearbeatthread.is_alive() and hearbeatthread.isStart == False:
            #             hearbeatthread.isStart =True
            #             hearbeatthread.start()
            # else:
                # print ("uav recv :",data.hex())
                #告警信息显示
                # print("msg:"+msg)

                # print("msg:"+msg)
                #mqttclient.publish("TEST/A", 'AAA')
            #等待5秒后进行 ，如果没有就主动发送心跳。
            # print("2222")
            
            # if  time.time()-startTime >5 and self.HeartbeatCheck ==0:
            #     if not hearbeatthread.is_alive() and hearbeatthread.isStart == False:
            #             hearbeatthread.isStart =True
            #             hearbeatthread.start()

            # print ("uav recv :",data.hex())
        # ('cmd_back2',ctypes.c_ubyte),#指令返回值2
            # result = mqttclient.publish(TOPIC_UAV, msg)
            # status = result[0]
            # if status == 0:
            #     print(f'Send `{msg}` to topic `{TOPIC_UAV}`')
            # else:
            #     print(f'Failed to `{mqttclient}`send message to topic {TOPIC_UAV}')
            # if uav.cmd_back1 != 0x00:
            # print ("head :%x %x %d"%(self.uavdata.cmd_back1,self.uavdata.cmd_back2,self.uavdata.length))

    def Send(self,data):
        try:
            global IsMaster
            if IsMaster != 1:
                return
            # print ("send:",data.hex())
            len =  self.uav_udp_socket.sendto(data, self.uav_addr)
        
            # print("Uav Sended :", str(len))
        except:
            print("Uav Sending Error!!!\n ")


     
#异步 无人机处理线程

class ReactUavThread(DatagramProtocol):
    def __init__(self ,id,recvport,targetip,targetport,iszubo):
        super(ReactUavThread,self).__init__()
        self.id = "uav_"+id
        self.targetip = targetip
        self.recvport = recvport
        self.targetport = targetport
        self.iszubo = iszubo

        
        self.lon =114.345317
        self.lat =38.0977876
        self.freq =0
        self.test_freq=0
        self.height=104

        r.set('uav',self.id) 
        r.hset(self.id,'lat', self.lat)
        r.hset(self.id,'lon', self.lon)
        r.hset(self.id,'height',self.height)

        # #接受无人机端口
        # if( iszubo == "1"):
        #     self.zubo_init(targetip,targetport,recvport)
        # else:
        #     self.dan_init(targetip,targetport,recvport)
        self.doFlyFile =None
        self.uavdata = Fight.Flight_Struct()
        self.locate=0.0
        self.mc=0.0
        self.v=0.0
        self.startTime = 0
        self.nextIndex=0
        self.lastIndex=0
        self.HeartbeatCheck = 0
        self.flightLength =0
        self.comfirmIndex =0
        self.mqttclient =None
        self.history_id = -1
        self.fps = 0
        self.iszubo = iszubo == "1"

        self.path_loaded = False
        #无人机 目标地址和端口
        self.uav_addr = (targetip, targetport)

        self.updateTime =time.time()
        global uavreplay

    
        #status init   
        r.hset(self.id, 'check','on') 
        r.hset(self.id, 'unlock','on')
        r.hset(self.id, 'lock','on') 
        r.hset(self.id, 'takeoff','on') 
        r.hset(self.id, 'return','on') 
        r.hset(self.id, 'land','on') 
        r.hset(self.id, 'light','on')
        r.hset(self.id, 'mode','on')
        r.hset(self.id, 'historyid',-1)
        r.hset(self.id, 'video','on') 
        r.hset(self.id, 'photo','on')
        r.hset(self.id, 'positioning','on')
        r.hset(self.id, 'hatch','on')
        r.hset(self.id, 'charging','on') 
        r.hset(self.id, 'wind_angle',0)
        r.hset(self.id, 'rain_snow',0)
        r.hset(self.id, 'out_temp',0)
        r.hset(self.id, 'in_temp',0)
        r.hset(self.id, 'mechanism','on')
        r.hset(self.id, 'pause','on') 
        r.hset(self.id, 'speed','on')

        self.heartbeat =Fight.Flight_HeartBeat()
        self.comfirm =Fight.Course_Confirm()
        self.path=Fight.Flight_Course_Struct()
        self.pathquery=Fight.Flight_Course_Query()
        self.check=Fight.Flight_Manage()
        self.startTime =time.time()
        # pod = Fight.Flight_Action()
        # data =pod.Unlock()
        # self.Send(message)
    def startProtocol(self):
        '''
        加入组播（必须重新）
        :return: 
        '''
        self.transport.setTTL(5) # 设置多播数据包的生存时间
        if self.iszubo:
            self.transport.joinGroup(self.targetip)
        # self.transport.write('Notify'.encode('utf8'),(self.targetip,self.targetport))

    def datagramReceived(self, todata: bytes, addr):
        '''
        接收到组播发送的数据
        :param datagram: 
        :param addr: 
        :return: 
        '''
        # history_id = self.
        # print("self.HeartbeatCheck "
       
        # offset =0
        # data =b''
        
        # a = hex(0xa5)
        # b = hex(0x5a)
        if self.doFlyFile is not None:
            self.doFlyFile.write(todata)
        
        # print("to offset"+str(offset))
        now = time.time()
        if now > self.updateTime+1:
            self.test_freq =self.freq
            self.freq = 0
            self.updateTime =time.time()
            # print ("ssss  "+str(self.test_freq ))
        else:
            self.freq +=1
           
        if self.doFlyFile is None and self.history_id != -1:
            filepath = './history/{}'.format(self.history_id)
            self.doFlyFile = open(filepath, 'wb')
            print("save file "+filepath)
            
        if self.history_id == -1 and self.doFlyFile is not None:
            self.doFlyFile.close()
            self.doFlyFile = None
            

        
        # if(len(todata) != 128):
            # print("to package {}: {}".format(len(todata), todata.hex()))

        ctypes.memmove(ctypes.addressof(self.self.heartbeat), todata, ctypes.sizeof(self.heartbeat))
        # print(" get cmd "+hex(self.heartbeat.cmd)+ "  "+hex(self.heartbeat.s_cmd))

        if(self.heartbeat.cmd == 0x08):
            print(" get heart beat ")
            # self.self.HeartbeatCheck =1
            # databuffer = databuffer[self.heartbeat.length:]
        elif(self.heartbeat.cmd == 0x05 and self.heartbeat.s_cmd == 0x22):
            # consolelog("update route")
            ctypes.memmove(ctypes.addressof(self.comfirm), todata, ctypes.sizeof(self.comfirm))
            # self.nextIndex  = struct.unpack('<H',data[5:7])
            self.nextIndex  =  self.comfirm.next
            # print("path self.comfirm",databuffer.hex())
            print("update route index ",self.comfirm.next)
            # databuffer = databuffer[comfirm.length:]

            if self.nextIndex ==  self.flightLength +1:
                print('-------------航线上传完成--------------')
                consolelog("航线上传完成")
                msg_dict ={'type':'loadsuccess'}
                msg = json.dumps(msg_dict)
                mqttclient.publish(TOPIC_INFO, msg)
                code =self.check.Check()
                uav.Send(code)
                
        
        elif(self.heartbeat.cmd == 0x05 and self.heartbeat.s_cmd == 0x41):
            ctypes.memmove(ctypes.addressof(self.pathquery), todata, ctypes.sizeof(self.pathquery))
            print("-----------------------------------recieve query",self.pathquery.index)
            try:
                # databuffer = databuffer[self.pathquery.length:]
                if self.pathquery.index <= self.flightLength:
                    if todata[6:24] == flightPath[self.pathquery.index-1][6:24]  and todata[28:30] == flightPath[self.pathquery.index-1][28:30]:
                        code =self.comfirm.PointComfirm(self.flightLength,self.pathquery.index)
                        uav.Send(code)
                        if(self.pathquery.index == uav.comfirmIndex):
                            consolelog("检查第 %d 个点 %.7f %.7f %.2f"%(self.pathquery.index ,self.pathquery.lon/pow(10,7),self.pathquery.lat/pow(10,7),self.pathquery.height/1000))
                            uav.comfirmIndex +=1
                        
                        # consolelog("check send",code.hex())
                        if self.pathquery.index == self.flightLength:
                            print("-------------航线装订成功--------------")
                            send_json_path()
                            self.path_loaded = True
                    else:
                        consolelog("第 %d 个点不一致"%self.pathquery.index)

                    
            except:
                print("Uav GET PATH Error!!!\n ")
                
            
        elif(self.heartbeat.cmd == 0x10 and self.heartbeat.s_cmd == 0x10):
            ctypes.memmove(ctypes.addressof(self.uavdata), todata, ctypes.sizeof(self.uavdata))
            truee = self.uavdata.CheckCRC(todata,self.uavdata.crc)
            # databuffer = databuffer[self.heartbeat.length:]
            print(todata.hex()+'----check is '+str(truee))

            self.lat = round(self.uavdata.lat/pow(10,7),8)
            self.lon = round(self.uavdata.lon/pow(10,7),8)
            self.height = self.uavdata.height
            
            r.hset(uav.id,'lat', self.lat)
            r.hset(uav.id,'lon', self.lon)
            r.hset(uav.id,'height',self.height)
            
       
            if  self.startTime + 2 < time.time():
                msg_dict ={'type':'drone','data': {
                'temp':self.uavdata.temp,
                'eng':self.uavdata.eng,
                'v':self.uavdata.v/10,
                'a':self.uavdata.a/10,
                'offset_staus':self.uavdata.offset_staus,
                'speed':self.uavdata.speed/100,
                'lat': round(self.uavdata.lat/pow(10,7),8),  #纬度
                'lon': round(self.uavdata.lon/pow(10,7),8) , #经度
                'height': self.uavdata.height,   #高度
                'rel_height':self.uavdata.rel_height/10,   
                'real_height':self.uavdata.real_height/100,
                'target_speed':self.uavdata.target_speed/100,
                'speed':self.uavdata.speed/100,   #地速x100
                'gps_speed':self.uavdata.gps_speed/100, 
                'trajectory':self.uavdata.trajectory/10,  #gui ji  jiao
                'pitch':self.uavdata.pitch /100,     #俯仰角
                'roll_angle':self.uavdata.roll_angle/100,  #滚转角
                'fu_wing':self.uavdata.fu_wing /100,
                'updown':self.uavdata.updown/100,
                'speedup':self.uavdata.speedup/100,
                'toward':self.uavdata.toward/100,    #航向角
                'lock':self.uavdata.lock,
                'toward_angle':self.uavdata.toward_angle/10,
                'fly_ctl':self.uavdata.fly_ctl,
                'staus':self.uavdata.staus,
                'fly_status':self.uavdata.fly_status,
                'gps_lost':self.uavdata.gps_lost,
                'link_lost':self.uavdata.link_lost,
                'area':self.uavdata.area,
                'turns_done':self.uavdata.turns_done,
                'turns_todo':self.uavdata.turns_todo,
                'fly_distance':self.uavdata.fly_distance,
                'fly_time':self.uavdata.fly_time,
                'target_point':self.uavdata.target_point,
                'target_height':self.uavdata.target_height/10,
                'target_angle':self.uavdata.target_angle/10,
                'stay_time':self.uavdata.stay_time,
                'flyctl_v':self.uavdata.flyctl_v/10,
                'engine_v':self.uavdata.engine_v/10,
                'gps_stars':self.uavdata.gps_stars,
                'year':self.uavdata.year,
                'month':self.uavdata.month,
                'day':self.uavdata.day,
                'hour':self.uavdata.hour,
                'min':self.uavdata.min,
                'sec':self.uavdata.sec,
                'flyctl_temp':self.uavdata.flyctl_temp,
                'offset_dist':self.uavdata.offset_dist,
                'HDOP':self.uavdata.HDOP/10,
                'VDOP':self.uavdata.VDOP/10,
                'SDOP':self.uavdata.SDOP/10,
                'height_cm':self.uavdata.height_cm,
                "freq":self.test_freq
                }
                }
                msg = json.dumps(msg_dict)
                
                if uav.uavdata.staus &(1<<1):
                    self.mc = 1
                else:
                    self.mc = 0
  
                if isset("mqttclient") == 1:
                    mqttclient.publish(TOPIC_INFO, msg)

          

    def closeConnection(self):
        '''
        自定义函数，离开组播时调用
        :return: 
        '''
        self.transport.leaveGroup()

    def Send(self,data):
        try:
            global IsMaster
            if IsMaster != 1:
                return
            # print ("send:",data.hex())
            # len =  self.uav_udp_socket.sendto(data, self.uav_addr)
            self.transport.write(data,(self.targetip,self.targetport))
        
            # print("Uav Sended :", str(len))
        except:
            print("Uav Sending Error!!!\n ")


#机场数据 处理数据
class AirportThread(threading.Thread):
    def __init__(self , ip ,port,rport):
        super(AirportThread,self).__init__()
        #接受机场数据端口
        print ("airport  :"+str(ip)+  "   " + str(port) + "   " + str(rport))
        self.zubo_init(ip,port,rport)
        self.airportdata = Fight.Airport_Receive()

    def zubo_init(self,ip ,port,rport):
        routeadd = "sudo route add -net "+ip+" netmask 255.255.255.255 dev "+eth
        # os.system(routeadd)
        os.system('echo %s | sudo -S %s' % (rootpassword, routeadd))


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # 允许端口复用
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # 绑定本机IP和组播端口
        self.sock.bind(('', rport))
        # 设置UDP Socket的组播数据包的TTL（Time To Live）值
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 255)
        # 声明套接字为组播类型
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_LOOP, 1)
        # 加入多播组
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP,
                             socket.inet_aton(ip) + socket.inet_aton('0.0.0.0'))
        #无人机 目标地址和端口
        self.airport_addr = (ip, port)

    def dan_init(self,ip ,port,rport):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        self.sock.bind(("", rport))
        
        #发送无人机创建UDP套接字
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #无人机 目标地址和端口
        self.airport_addr = (ip, port)
        
    def run(self):
        
        while True:
            # print ("airport recv ---:")

            data, addr = self.sock.recvfrom(1024)      # buffer size is 4096 bytes
            ctypes.memmove(ctypes.addressof(self.airportdata), data, ctypes.sizeof(self.airportdata))
            # print('from '+str(airport.airportdata.warehouse_status))

            msg_dict ={'type':'hangar','data': {
                'battery_v':self.airportdata.battery_v,   #电池电压
                'battery_temp': self.airportdata.battery_temp,   #电池温度
                'hatch': self.airportdata.warehouse_status,    #舱盖状态
                'homing': self.airportdata.homing_status,  #归位装置状态
                'charge': self.airportdata.battery_status, #充电状态
                'uavpower_status':self.airportdata.uavpower_status,   #无人机电源状态
                'gps_stars' :uav.uavdata.gps_stars ,   #GPS星数
                #'fps' :uav.uavdata.fps ,   #GPS星数
                'fps' :0 ,   #GPS星数
                'wind_angle' : self.airportdata.wind_angle,   #风向
                #7	6	5	4	3	2	1	0
                #北风	东北风	东风	东南风	南风	西南风	西风	西北风
                'rain_snow' : self.airportdata.rain_snow,   ##雨雪传感器  1在下雨 0不在下雨
                'out_temp' : self.airportdata.out_temp,   #舱外温度
                'out_humidity' : self.airportdata.out_humidity,   #舱外湿度
                'in_temp' : self.airportdata.battery_status,   #舱内温度
                'in_humidity' : self.airportdata.battery_status,   #舱内湿度
            }
            }
            r.hset(uav.id, 'wind_angle',self.airportdata.wind_angle)
            r.hset(uav.id, 'rain_snow',self.airportdata.rain_snow)
            r.hset(uav.id, 'out_temp',self.airportdata.out_temp)
            r.hset(uav.id, 'in_temp',self.airportdata.in_temp)
            msg = json.dumps(msg_dict)
            # print("aireport:"+msg)
            # print("self.mqttclient:",mqttclient)
            mqttclient.publish(TOPIC_INFO, msg)
            # status = result[0]
            
            # print ("airport recv :",data.hex())

            # print ("head :%x %x %d"%(airport.head,airport.head2,airport.length))
    def Send(self,data):
        try:
            global IsMaster
            if IsMaster != 1:
                return
            # print ("send:",data.hex())
            len =  self.sock.sendto(data, self.airport_addr)
            # print("Airport Sended " + str(len))
        except:
            print("Airport Sending Error!!!\n")
            

#摄像头处理线程
class CameraThread(threading.Thread):
    def __init__(self , camip,camport):
        super(CameraThread,self).__init__()
        self.dan_init(camip,camport)
        self.updateTime =time.time()

        # self.Send(message)
    def zubo_init(self,ip ,port,rport):
        routeadd = "sudo route add -net "+ip+" netmask 255.255.255.255 dev "+eth
        # os.system(routeadd)
        os.system('echo %s | sudo -S %s' % (rootpassword, routeadd))


        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

        # 允许多个socket绑定到同一个端口号
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        # 绑定到对应的地址和端口上
        self.sock.bind(('', rport))

        # 告诉操作系统将socket加入指定的组播组
        mreq = struct.pack("4sl", socket.inet_aton(ip), socket.INADDR_ANY)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, mreq)

        # 设置超时时间，如果需要可以省略
        self.sock.settimeout(5)
        #无人机 目标地址和端口
        self.cam_addr = (ip, port)

    def dan_init(self,ip ,port):
        self.sock  = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        self.sock .bind(("", port))
        
        #发送无人机创建UDP套接字
        self.cam_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cam_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #无人机 目标地址和端口
        self.cam_addr = (ip, port)

    def run(self):
        cam_data = Fight.Pod_Receive()
        databuffer =b''
       
        offset =0
        data =b''
 
        while True: 
            databuffer =b''
           
            if(len(databuffer) == 0):
                data, _ = self.sock.recvfrom(32)      # buffer size is 4096 bytes
                # print(" ：Received message  {}: {}".format(len(data), data))

            else:
                data = databuffer

            offset =0
            index =0
           
            while offset < len(data):
                byte =data[offset]
                byte2 =0
                if offset < len(data)-1:
                    byte2 = data[offset+1]
                if hex(byte) == 0xfc and hex(byte2) == 0x2c :
                    index = offset
                    break
                offset +=1
                    
            
            # if foundheader2 and len(databuffer) == 0:
            databuffer=data[index:]
            
            while(len(databuffer)< ctypes.sizeof(cam_data)):
                data, _ = self.sock.recvfrom(32)      # buffer size is 4096 bytes
                databuffer+=data
          
            self.updateTime =time.time()
            # print("to offset"+str(offset))
            todata=bytes(bytearray(databuffer))
            # print('from '+str(addr))
            ctypes.memmove(ctypes.addressof(cam_data), todata, ctypes.sizeof(cam_data))
            # print ("cam recv :",cam_data.type)
            if cam_data.type == 0x04:
        
                msg_dict ={'type':'monitor','data': {
                    'lon':round(cam_data.lon,8),  #target经度
                    'lat':round(cam_data.lat,8),    #target纬度
                    'target_height': cam_data.target_height,  #target高度
                    'tf_total': cam_data.tf_total/10,   #TF卡总容量
                    'tf_usage':cam_data.tf_usage,   #TF卡使用容量百分比 0-100%  
                    'lon':cam_data.lon,  
                    'lat':cam_data.lat,  
                    'target_height':cam_data.target_height,  
                }
                }
                msg = json.dumps(msg_dict)
                # print(msg)
                global mqttclient
                # result = mqttclient.publish(TOPIC_INFO, msg)
                if mqttclient:
                    mqttclient.publish(TOPIC_INFO, msg)

                # print ("cam  :%s"%(msg))


    def Send(self,data):
        try:
            global IsMaster
            if IsMaster != 1:
                return
            # print ("send:",data.hex())
            len =  self.cam_udp_socket.sendto(data, self.cam_addr)
            # print("Cam Sended " + str(len))
        except:
            print("Cam Sending Error!!!\n")

#云台控制
    def SendPTZ(self,dir,pitch,tracking):
        try:
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
            len =  self.cam_udp_socket.sendto(data, self.cam_addr)
            # print("Cam Sended " + str(len))
        except:
            print("Cam Sending Error!!!\n")
        
# 无人机ip  发送端口 接收端口 载荷ip  载荷 端口
#  client.py 192.168.8.200 14551 14550 192.168.8.160 10000 226.0.0.80 20001 20002 rtsp://127.0.0.1/live/test
if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    # 添加位置参数
    parser.add_argument("id", help="uav id")
    parser.add_argument("ip", help="uav ip here")
    parser.add_argument("port", help="uav port...", type=int)
    parser.add_argument("r_port", help="uav port...", type=int)
    parser.add_argument("monitor_ip", help="cam ip here")
    parser.add_argument("monitor_port", help="cam port...", type=int)
    parser.add_argument("airport_ip", help="airport ip here")
    parser.add_argument("airport_port", help="airport port...", type=int)
    parser.add_argument("airport_rport", help="airport recvport...", type=int)
    # parser.add_argument("camera_url", help="camera url ...")
    parser.add_argument("uav_zubo", help="uav url ...")
    parser.add_argument("network", help="eth url ...")
    parser.add_argument("joystick", help="joystick  ...")
    

    # parser.add_argument("steam_url", help="uav camera video steam")

    args = parser.parse_args()

    print('UAV Connect' + args.ip + " "+ str(args.port) +" "+ str(args.r_port) + " Camera :"+args.monitor_ip + " "+str(args.monitor_port) +
          " Airport :"+args.airport_ip + " "+str(args.airport_port) +" uav_zubo "+str(args.uav_zubo)+" eth  "+str(args.network)+" joystick  "+str(args.joystick))
    eth = args.network
    joystick = args.joystick
    # try:
    print ("uav thread")
    global uav
    # uav = UavThread(args.id,args.r_port,args.ip,args.port,args.uav_zubo)
    # uav.start()
    uav = ReactUavThread(args.id,args.r_port,args.ip,args.port,args.uav_zubo)
    reactor.listenMulticast(args.r_port,uav,args.uav_zubo == '1')
    
    try:
        print ("camera thread")
        global cam
        cam = CameraThread(args.monitor_ip,args.monitor_port)
        cam.start()
    except:
        print("start CameraThread Error!!!\n ")
        
    try:
        #机场连接
        print ("airport thread")
        global airport
        airport = AirportThread(args.airport_ip,args.airport_port,args.airport_rport)
        airport.start()
    except:
        print("start AirportThread Error!!!\n ")
        # 心跳发送
        print ("Hearbeat thread")
        
    try:
        global hearbeatthread
        hearbeatthread = HearbeatThread()
        hearbeatthread.start()
    
    except:
        print("start HearbeatThread Error!!!\n ")

    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    host = '127.0.0.1'


    loop.run_until_complete(mqttconnect(host))

    reactor.run()

    # uav.join()
    # cam.join()
    
    # airport.join()
    print ("after camera")
    loop.stop()
    loop.close()
    # uav_udp_socket.close()