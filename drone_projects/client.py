from filecmp import cmp
import os
import socket
import struct
import ctypes
import json
import asyncio
import copy
import signal
import time
import webSocket.flight as Fight
import webSocket.crc16 as crc16
import numpy as np
# import drone_yolov8_deploy_noshow as yolo
import argparse
# from paho.mqtt import client as mqtt_client
import threading
from gmqtt import Client as MQTTClient
import redis
from goto import with_goto

BROKER = '127.0.0.1'
PORT = 1883
TOPIC_INFO = "info"
TOPIC_ALERT = "alert/#"
TOPIC_CONSOLE = "console" #命令数据
TOPIC_CTRL    = "control" #命令
TOPIC_STATE = "state"
FLY_CTRL = "fly_control"



CLIENT_ID = f'pushuav222222'
USERNAME = ''
PASSWORD = ''

r = redis.Redis(host='127.0.0.1',port=6379,db=0)

r.hset('drone', 'check','on') 
r.hset('drone', 'unlock','on')
r.hset('drone', 'lock','on') 
r.hset('drone', 'takeoff','on') 
r.hset('drone', 'return','on') 
r.hset('drone', 'land','on') 
r.hset('drone', 'light','on')
r.hset('drone', 'mode','on')
r.hset('drone', 'historyid',-1)
r.hset('monitor', 'video','on') 
r.hset('monitor', 'photo','on')
r.hset('monitor', 'positioning','on')
r.hset('hangar', 'hatch','on')
r.hset('hangar', 'charging','on') 
r.hset('hangar', 'mechanism','on')
r.hset('player', 'HistoryID',-1)
r.hset('player', 'pause','on') 
r.hset('player', 'speed','on')

#无人机
#经度
lon=0
#纬度 
lat=0 
#高度
height  =0


#是否是启动回放
isReplay  =0

#前端控制播放位置 > 0
doSeek  =-1

#is main control device ， == 1 can send message，or only listen data
IsMaster =0
#自检
SelfCheck =0#1  0失败 1成功
# 心跳check
# HeartbeatCheck =0#1

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
history_id =0

STOP = asyncio.Event()

flightPath=[]


def consolelog(msg):
    print(msg)
    mqttclient.publish(TOPIC_CONSOLE, msg)


#发送航线
#异常处理，进程崩溃，恢复，发现飞机在飞行中，回复检查点，状态机，流程点。
@with_goto
async def go_fly(path,historyid):
    global history_id
    history_id =historyid
    # r.sestnx('fly',0)
    # hisfly= r.get('fly')
    consolelog("气象判断")
    # if hisfly > 0:
    #     goto .land
    if True:
        consolelog("气象没问题")

    await asyncio.sleep(2)

    # if airport.rain_snow == False:
    #print('气象没问题')

    # if airport.uavpower_status == 0:
    consolelog("点位正常")
    await asyncio.sleep(2)

    
    # r.hset('drone','historyid',history_id)
    
    await OpenAirport()
    consolelog("发送机场开仓指令")

    await asyncio.sleep(1)

    #发送航线数据
    # print('无人机定位数据' + str(uav.uavdata.lon) + "  "+str(uav.uavdata.lat) )
    consolelog('无人机定位数据 : ' + str(uav.uavdata.lon) + "  "+str(uav.uavdata.lat) )
    # while(uav.uavdata.lon != 0 and uav.uavdata.lat != 0 ):
    #     time.sleep(1)
    await RunSelfCheck()
    consolelog("装订航线")
    label .send_path
    # a =[path]
    # print (a)
    re = await send_path(path)
    if re ==0:
        return
    await asyncio.sleep(1)

    label .selfcheck
    consolelog("发送程控指令")
    await SendProgramControl()
    
    await asyncio.sleep(1)
    consolelog("发送无人机解锁指令")
    await UnlockFlight()
    # #飞行结束
    # label .needend
    await asyncio.sleep(1)
    
    consolelog('舱盖是否开关' +airport.airportdata.warehouse_status)  
    # print('舱盖是否开关' +airport.airportdata.warehouse_status)
    # while (airport.airportdata.warehouse_status != 1)
    #     time.sleep(1)
    await asyncio.sleep(3)


    consolelog('舱盖已经打开')
    #开仓门，成功
    await OpenAirport()

    # r.hmset('fly',{'history_id':history_id, 'status': 3})
    await asyncio.sleep(3)
    #降落
    consolelog('舱盖已经打开')

    await ReturnBack()
    consolelog('飞机降落')
    
    await asyncio.sleep(3)

    await CloseAirport()
    consolelog('关闭机库')
    
    msg ="{'cmd':'fly_over':{'history_id':{}}}".format(history_id)
    mqttclient.publish(FLY_CTRL, msg)
    r.hdel('fly')
    
    label .end
    consolelog("任务完成 ")

#发送程控
async def SendProgramControl():
    pod = Fight.Flight_Action()
    data =pod.AutomaticControl()
    print("automatic")
    uav.Send(data)  
    r.hset('drone','mode','off')
    return 1

#解锁指令
async def UnlockFlight():
    pod = Fight.Flight_Action()
    data =pod.Unlock()
    uav.Send(data)
    r.hset('drone','unlock','off')
    return 1

#起飞
async def Takeoff():
    pod = Fight.Flight_Action()
    data =pod.Land()
    uav.Send(data) 
    r.hset('drone','land','off')
    return 1

#返回
async def ReturnBack():
    pod = Fight.Flight_Action()
    data =pod.Return()
    uav.Send(data)  
    r.hset('drone','return','off')

#系统自检
async def RunSelfCheck():
    global SelfCheck
    SelfCheck = 1
    #电池电压  (配置文件的电池电压参数)
    if SelfCheck == 1 :
        if uav.uavdata.v < 44:
            SelfCheck =0 
            print("电压自检失败")
        else:
            SelfCheck =1
            print("电压自检successfull")

    
    # 定位状态
    if SelfCheck == 1 :
        if uav.uavdata.offset_staus == 0:
            SelfCheck =0 
            print("定位自检失败")
        else:
            SelfCheck = 1
            print("定位自检successfull")

    # 丢星时间
    if SelfCheck == 1 :
        if uav.uavdata.gps_lost > 0:
            SelfCheck =0 
            print("丢星时间自检失败")
        else:
            SelfCheck = 1
            print("丢星successfull")

    # 俯仰角
    if SelfCheck == 1 :
        if uav.uavdata.pitch/100 > 3:
            SelfCheck =0 
            print("俯仰角自检失败")
        else:
            SelfCheck = 1
            print("俯仰角自检successfull")

    # 横滚角
    if SelfCheck == 1 :
        # print(uav.uavdata.roll_angle)
        if uav.uavdata.roll_angle/100 > 3:
            SelfCheck =0 
            print("横滚角自检失败")
        else:
            SelfCheck = 1
            print("横滚角自检successfull")

    # 磁罗盘连接 无人机遥测信息第71-72字节第二位是不是1 不是1则异常
    if SelfCheck == 1 :
        if uav.mc != 1:
            SelfCheck =0 
            print("磁罗盘连接自检失败")
        else:
            SelfCheck = 1
            print("磁罗连接successfull")

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
            print("测向自检失败")
        else:
            SelfCheck = 1
            print("测向自检successfull")
            

    # 舱盖状态
    if SelfCheck == 1 :
        if airport.airportdata.warehouse_status != 2: 
            SelfCheck =0 
            print("舱盖自检失败")
        else:
            SelfCheck = 1
            print("舱盖自检successfull")

    # 归机机构状态
    if SelfCheck == 1 :
        if airport.airportdata.homing_status != 2: 
            SelfCheck =0 
            print("归机机构自检失败")
        else:
            SelfCheck = 1
            print("归位自检successfull")

    # 自检完成  
    if SelfCheck == 1:
        print("自检完成")
        msg_dict ={'type':'selfchecksuccess'}
        msg = json.dumps(msg_dict)
        mqttclient.publish(TOPIC_INFO, msg)
        r.hset('drone','check','off')
                
#开仓门
async def OpenAirport():
    pod = Fight.Hatch_control()
    data =pod.OpenHatch()
    airport.Send(data) 
    r.hset('hangar','hatch','off')
    return 1

#关仓门
async def CloseAirport():
    pod = Fight.Hatch_control()
    data =pod.CloseHatch()
    airport.Send(data) 
    r.hset('hangar','hatch','on')
    return 1

#发送航线
async def send_path(path):
    #发送航线数据
    global flightPath
    # flightPath =copy.deepcopy(path)
    pod = Fight.Flight_Course_Struct()
    # print("path "+path[0])
    data =pod.PathUpdate(path[0]['coord'][0],path[0]['coord'][1],path[0]['coord'][2],path[0]['speed'],path[0]['hovertime'],path[0]['radius'],
                         path[0]['photo'],path[0]['heightmode'],path[0]['turning'],len(path),1)
    uav.Send(data) 
    print("no.1 path",data.hex())
    flightPath.clear()
    #save senddata
    flightPath.append(data)

    length = len(path)
    uav.lastIndex =1
    uav.flightLength =length
    while uav.lastIndex < length :
        try:
            # uav.nextIndex = Fight.Course_Confirm.next
            # if input() == 'c':
            #     break
            # print(uav.lastIndex , uav.nextIndex)
            # if uav.lastIndex-1 == uav.nextIndex:
            #     pod = Fight.Flight_Course_Struct()
            #     # data =pod.PathUpdate(path[uav.nextIndex].lat,path[uav.nextIndex].lon,path[uav.nextIndex].height,path[uav.nextIndex].speed,
            #     #                      path[uav.nextIndex].hovertime,path[uav.nextIndex].radius,path[uav.nextIndex].totalnum,path[uav.nextIndex].num)
            #     # data =pod.PathUpdate(path[uav.nextIndex-1].coord[0],path[uav.nextIndex-1].coord[1],path[uav.nextIndex-1].coord[2],
            #     #                      path[uav.nextIndex-1].speed,path[uav.nextIndex-1].hovertime,path[uav.nextIndex-1].radius,
            #     #                      path[uav.nextIndex-1].photo,path[uav.nextIndex-1].heightmode,path[uav.nextIndex-1].turning,
            #     #                      len(path),uav.nextIndex-1)
            #     data =pod.PathUpdate(path[uav.nextIndex]['coord'][0],path[uav.nextIndex]['coord'][1],path[uav.nextIndex]['coord'][2],
            #                          path[uav.nextIndex]['speed'],path[uav.nextIndex]['hovertime'],path[uav.nextIndex]['radius'],
            #                          path[uav.nextIndex]['photo'],path[uav.nextIndex]['heightmode'],path[uav.nextIndex]['turning'],len(path),uav.nextIndex)
            #     uav.Send(data) 
            #     print(data.hex())
            #     # uav.lastIndex = uav.nextIndex
            # print(uav.lastIndex,uav.nextIndex)
            
            if uav.nextIndex == 0 :
                await asyncio.sleep(3)

            if uav.nextIndex == 0 :
                pod = Fight.Flight_Course_Struct()
                data =pod.PathUpdate(path[0]['coord'][0],path[0]['coord'][1],path[0]['coord'][2],path[0]['speed'],path[0]['hovertime'],path[0]['radius'],
                            path[0]['photo'],path[0]['heightmode'],path[0]['turning'],len(path),1)
                uav.Send(data) 
                print("repeat",data.hex())
                

            if uav.lastIndex+1 == uav.nextIndex:
                uav.lastIndex = uav.nextIndex
                pod = Fight.Flight_Course_Struct()
                # data =pod.PathUpdate(path[uav.nextIndex].lat,path[uav.nextIndex].lon,path[uav.nextIndex].height,path[uav.nextIndex].speed,
                #                      path[uav.nextIndex].hovertime,path[uav.nextIndex].radius,path[uav.nextIndex].totalnum,path[uav.nextIndex].num)
                # data =pod.PathUpdate(path[uav.nextIndex-1].coord[0],path[uav.nextIndex-1].coord[1],path[uav.nextIndex-1].coord[2],
                #                      path[uav.nextIndex-1].speed,path[uav.nextIndex-1].hovertime,path[uav.nextIndex-1].radius,
                #                      path[uav.nextIndex-1].photo,path[uav.nextIndex-1].heightmode,path[uav.nextIndex-1].turning,
                #                      len(path),uav.nextIndex-1)
                data =pod.PathUpdate(path[uav.nextIndex-1]['coord'][0],path[uav.nextIndex-1]['coord'][1],path[uav.nextIndex-1]['coord'][2],
                                    path[uav.nextIndex-1]['speed'],path[uav.nextIndex-1]['hovertime'],path[uav.nextIndex-1]['radius'],
                                    path[uav.nextIndex-1]['photo'],path[uav.nextIndex-1]['heightmode'],path[uav.nextIndex-1]['turning'],len(path),uav.nextIndex)
                uav.Send(data)
                flightPath.append(data)
                print("-----send ",data.hex()) 
            
        except KeyboardInterrupt:
            print("exit....")
            break


#回放数据
def replay(history):
    global uavreplay
    global isReplay
    uavreplay = UavReplayThread(history)
    uavreplay.start()
    isReplay =1
     
def stop():
    global uavreplay
    global isReplay
    uavreplay.isStop = True
    isReplay =0


def pause():
    global uavreplay
    global isReplay
    uavreplay.isPause = True
    isReplay =1

def next():
    global uavreplay
    global isReplay
    uavreplay.isPause = False
    isReplay =1

def seek(pos):
    global doSeek
    doSeek = pos/100.0

    
#系统当前状态
def send_state():
    # HIS = HistoryID
    msg_dict ={
        'drone': {  
            "check": { "data": r.hget('drone', 'check') .decode()},
            "unlock": { "data": r.hget('drone', 'unlock') .decode()},         
            "lock": { "data": r.hget('drone', 'lock') .decode()},
            "takeoff": { "data": r.hget('drone', 'takeoff') .decode()},
            "return": { "data": r.hget('drone', 'return') .decode()},
            "land": { "data": r.hget('drone', 'land') .decode()},
            "light": { "data": r.hget('drone', 'light') .decode()},
            "mode": { "data": r.hget('drone', 'mode') .decode()},
            "historyid": { "data": int(r.hget('drone', 'historyid') .decode())}
        },
        'monitor': { 
            "video": { "data": r.hget('monitor', 'video') .decode()},
            "photo": { "data": r.hget('monitor', 'photo') .decode()},
            "positioning": { "data": r.hget('monitor', 'positioning') .decode()}
        },
        'hangar':{ 
            "hatch": { "data": r.hget('hangar', 'hatch') .decode()},
            "charging": { "data": r.hget('hangar', 'charging') .decode()},
            "mechanism": { "data": r.hget('hangar', 'mechanism') .decode()}
        },
        'player':{ 
            "play": { "data":int(r.hget('player', 'HistoryID').decode())},
            "pause": { "data": r.hget('player', 'pause') .decode()},
            "speed": { "data":  r.hget('player', 'speed') .decode()}
        }
    }
    # print("-----send ",msg_dict) 
    msg = json.dumps(msg_dict)
    mqttclient.publish(TOPIC_STATE, msg)

#定点巡航
def send_pointpath(point):
    pod = Fight.Course_Set_Struct()
    data =pod.point(point['coord'][0],point['coord'][1],point['coord'][2],point["radius"],point['time'],point['direction'],point['mode'],point['speed'])
    uav.Send(data)    
    print('send pointpath successed')


async def on_message(client, topic, payload, qos, properties):
    print(f'RECV MSG: {topic} {payload}')
    # try:
    jsondata = json.loads(payload)
    
    # result = cmp(jsondata['cmd'], 'snapshot')
    cmd = jsondata['cmd']
    param = jsondata['data']

    # # 摄像头心跳 空指令
    # pod = Fight.Pod_Send()
    # add = uav.uavdata
    # data =pod.CleanUp(add.pitch/100,add.roll_angle/100,add.toward_angle,add.lon,add.lat,add.gps_stars,add.height,add.speed/100,add.rel_height/10)
    # cam.Send(data) 
    # await time.sleep(0.04)
    # cam.Send(data) 

    if topic ==TOPIC_CTRL:
        #系统状态
        history = jsondata['historyid']
        if  cmd =='dofly':
            await(go_fly(param,history))


        #系统状态
        if  cmd =='state':
            send_state()

        #启动回放
        if  cmd =='player/play':
            replay(param)
            r.hset('player','HistoryID',param)
            
            
        #退出回放
        if  cmd =='player/stop':
            stop()

        #暂停回放
        if  cmd =='player/pause' and param == 'on':
            pause()
            r.hset('player','pause','off')

        #继续回放
        if  cmd =='player/pause'and param == 'off':            
            next()
            r.hset('player','pause','on')
        

        #调整播放倍速
        if  cmd == 'player/speed':
            uavreplay.speed=(1/param)
            r.hset('player','speed',param)

        #播放位置调整
        if  cmd =='player/seek':
            seek(param)


        #航线指令##

        #航线加载
        if  cmd =='drone/route':
            await send_path(param)

        #航线圈数
        if  cmd =='drone/circle':
            # circle = param
            pod = Fight.Flight_Circle_Struct()
            data =pod.turns(param)
            uav.Send(data)

        #定点巡航
        if  cmd =='drone/point':
            send_pointpath(param)

        ##无人机指令##
        global SelfCheck
        if  cmd == 'drone/check':
            await(SelfCheck())
        

        if SelfCheck == 1:
            if cmd == 'drone/unlock' :
                pod = Fight.Flight_Action()
                data =pod.Unlock()
                uav.Send(data)
                r.hset('drone','unlock','off')

            elif cmd == 'drone/takeoff':
                pod = Fight.Flight_Action()
                data =pod.TakeOff()
                uav.Send(data)
                r.hset('drone','takeoff','off')

            elif cmd == 'drone/lock':
                pod = Fight.Flight_Action()
                data =pod.Lock()
                uav.Send(data) 
                r.hset('drone','lock','off')

            elif cmd == 'drone/mode' and param =='automatic':
                pod = Fight.Flight_Action()
                data =pod.AutomaticControl()
                print("automatic")
                uav.Send(data)  
                r.hset('drone','mode','off')

            elif cmd == 'drone/mode' and param =='manual':
                pod = Fight.Flight_Action()
                data =pod.ManualControl()
                print("manual")
                uav.Send(data) 
                r.hset('drone','mode','on')

            elif cmd == 'drone/return':
                pod = Fight.Flight_Action()
                data =pod.Return()
                uav.Send(data)  
                r.hset('drone','return','off')

            elif cmd == 'drone/land':
                pod = Fight.Flight_Action()
                data =pod.Land()
                uav.Send(data) 
                r.hset('drone','land','off')

            elif cmd == 'drone/light' and param =='on':
                pod = Fight.Flight_Action()
                data =pod.Anticollision_Light_On()
                uav.Send(data) 
                r.hset('drone','light','off')

            elif cmd == 'drone/light' and param =='off':
                pod = Fight.Flight_Action()
                data =pod.Anticollision_Light_Off()
                uav.Send(data)
                r.hset('drone','light','on')
                
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

        ##载荷指令##
        if cmd == 'monitor/up':
            pod = Fight.Pod_Send()
            data =pod.FieldUp()
            cam.Send(data) 
            hearbeatthread.camData=1

        elif cmd == 'monitor/down':
            pod = Fight.Pod_Send()
            data =pod.FieldDown()
            cam.Send(data)
            hearbeatthread.camData=1

        elif cmd == 'monitor/left':
            pod = Fight.Pod_Send()
            data =pod.FieldLeft()
            cam.Send(data)     
            hearbeatthread.camData=1

        elif cmd == 'monitor/right':
            pod = Fight.Pod_Send()
            data =pod.FieldRight()
            cam.Send(data) 
            hearbeatthread.camData=1

        elif cmd == 'monitor/centering':
            pod = Fight.Pod_Send()
            data =pod.Centering()
            # print(data.hex())
            cam.Send(data)   
            r.hset('monitor','centering','off')  
        
        elif cmd == 'monitor/photo':
            pod = Fight.Pod_Send()
            data =pod.Photo()
            cam.Send(data) 
            r.hset('monitor','photo','off') 

        elif cmd == 'monitor/video' and param =='on':
            pod = Fight.Pod_Send()
            data =pod.Video()
            cam.Send(data) 
            r.hset('monitor','video','off')  

        elif cmd == 'monitor/video' and param =='off':
            pod = Fight.Pod_Send()
            data =pod.Video()
            cam.Send(data) 
            r.hset('monitor','video','on')  

        elif cmd == 'monitor/view+':
            pod = Fight.Pod_Send()
            data =pod.LargenField()
            cam.Send(data)
            hearbeatthread.camData=1

        elif cmd == 'monitor/view-':
            pod = Fight.Pod_Send()
            data =pod.ReduceField()
            cam.Send(data) 
            hearbeatthread.camData=1

        elif cmd == 'monitor/focus+':
            pod = Fight.Pod_Send()
            data =pod.FocusUp()
            cam.Send(data) 
            hearbeatthread.camData=1

        elif cmd == 'monitor/focus-':
            pod = Fight.Pod_Send()
            data =pod.FocusDown()
            cam.Send(data) 
            hearbeatthread.camData=1
        
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
            r.hset('monitor','positioning','off')

        elif cmd == 'monitor/positioning'and param =='off':
            pod = Fight.Pod_Send()
            data =pod.CloseLaser(uav.uavdata.pitch,uav.uavdata.roll_angle,uav.uavdata.toward_angle,uav.uavdata.lon,uav.uavdata.lat,uav.uavdata.height,uav.uavdata.rel_height)
            cam.Send(data) 
            r.hset('monitor','positioning','on')

        elif cmd == 'monitor/tracking':
            pod = Fight.Pod_Send()
            data =pod.Tracking(uav.uavdata.pitch,uav.uavdata.roll_angle,uav.uavdata.toward_angle,uav.uavdata.lon,uav.uavdata.lat,uav.uavdata.height,uav.uavdata.rel_height)
            cam.Send(data) 
            r.hset('monitor','tracking','off')

        elif cmd == 'monitor/collect':
            pod = Fight.Pod_Send()
            data =pod.Collect()
            cam.Send(data) 
            r.hset('monitor','collect','off')

        elif cmd == 'monitor/downward':
            pod = Fight.Pod_Send()
            data =pod.Downward()
            cam.Send(data) 
            r.hset('monitor','downward','off')

        elif cmd == 'monitor/scanning':
            pod = Fight.Pod_Send()
            data =pod.Scanning()
            cam.Send(data) 
            r.hset('monitor','scanning','off')

        elif cmd == 'monitor/imageswitch':
            pod = Fight.Pod_Send()
            data =pod.ImageSwitch()
            cam.Send(data) 
            r.hset('monitor','imageswitch','off')

        ##机场指令##
        elif cmd == 'hangar/hatch'and param =='on':
            pod = Fight.Hatch_control()
            data =pod.OpenHatch()
            airport.Send(data) 
            r.hset('hangar','hatch','off')


        elif cmd == 'hangar/hatch'and param =='off':
            pod = Fight.Hatch_control()
            data =pod.CloseHatch()
            airport.Send(data) 
            r.hset('hangar','hatch','on')

        #归位锁定   
        elif cmd == 'hangar/mechanism'and param =='on':
            pod = Fight.Homing_control()
            data =pod.HomeLock()
            airport.Send(data) 
            r.hset('hangar','mechanism','off')

        #归位解锁
        elif cmd == 'hangar/mechanism'and param =='off':
            pod = Fight.Homing_control()
            data =pod.HomeUnlock()
            airport.Send(data) 
            r.hset('hangar','mechanism','on')
    

        elif cmd == 'hangar/charging'and param =='on':
            pod = Fight.Charge_control()
            data =pod.Charge()
            airport.Send(data) 
            r.hset('hangar','charging','off')


        elif cmd == 'hangar/charging'and param =='off':
            pod = Fight.Charge_control()
            data =pod.ChargeOff()
            airport.Send(data) 
            r.hset('hangar','charging','on')
        send_state()


    
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
    mqttclient = MQTTClient("client-id222")

    mqttclient.on_connect = on_connect
    mqttclient.on_message = on_message
    mqttclient.on_subscribe = on_subscribe
    mqttclient.on_disconnect = on_disconnect

    # Connectting the MQTT brokewarehouser
    await mqttclient.connect(broker_host)

    # Subscribe to topic
    mqttclient.subscribe(TOPIC_CTRL)

    # Send the data of test
    # mqttclient.publish("TEST/A", 'AAA')
    # mqttclient.publish("TEST/A", 'BBB')

    await STOP.wait()
    await mqttclient.disconnect()


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
            if self.uav_time +1 < current:
                global IsMaster
                IsMaster = 1
                data = hb.SendHeartBeat()
                uav.Send(data)
                self.uav_time=current
                # self.uav_num += 1 
                # print("已发送heartbeat次数:",self.uav_num)

            if self.cam_time + 0.2< current and self.camData is None:
                
                data = pod_hb.Cambeat(uav.uavdata.pitch,uav.uavdata.roll_angle,uav.uavdata.toward_angle,uav.uavdata.lon,uav.uavdata.lat,
                                      uav.uavdata.height,uav.uavdata.rel_height,uav.uavdata.gps_stars)
                cam.Send(data)
                self.cam_time =current
                # self.cam_num += 1 
                # print("已发送cambeat次数:",self.cam_num)


#无人机回放数据
class UavReplayThread(threading.Thread):
    def __init__(self ,history_id):
        super(UavReplayThread,self).__init__()
        self.history_id = history_id
        self.isStop =False
        self.isPause = False
        self.speed =1

    def run(self):
        test=Fight.Flight_REPLAY_Struct()
        
        global doSeek
        history_file = 'history/{}'.format(self.history_id)
        print("start replay file "+history_file)
        f =open(history_file, 'rb')
        f.seek(0, os.SEEK_END) 
        filelen = f.tell()
        f.seek(0, os.SEEK_SET) 
        a = int('a5',16)
        b = int('5a',16)
        cmd = int('10',16)
        print("read " )

        while self.isStop ==False:
            while self.isPause ==False:
                # print(self.isStop)
                if(doSeek>=0):
                    f.seek(int(filelen * doSeek))
                    doSeek = -1
                    
                data = f.read(1)
                head = struct.unpack("B", data)
                # print("=0x%x "%(head))
                if a == int.from_bytes(head, byteorder='little'):
                    # print("=0x%x "%(head))
                    data = f.read(1)
                    head2 = struct.unpack("B", data)
                    if b == int.from_bytes(head2, byteorder='little'):
                        print("->0x%x"%(head2))
                        lenc = f.read(1)
                        len2 = struct.unpack("B", lenc)
                        len = int.from_bytes(len2, byteorder='little')

                        data = f.read(1)
                        rcmd = struct.unpack("B", data)
                        #left length
                        if  cmd == int.from_bytes(rcmd, byteorder='little') and len == 128:
                            
                            left = len -4
                            data = f.read(left)
                            ctypes.memmove(ctypes.addressof(test), data, ctypes.sizeof(test))
            
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
                                'height_cm':test.height_cm

                                }
                            }
                            

                            msg = json.dumps(msg_dict)
                            print("msg ->"+msg)
                
                            mqttclient.publish(TOPIC_INFO, msg)
                            time.sleep(self.speed)

            
#无人机处理线程
class UavThread(threading.Thread):
    def __init__(self ,recvport,targetip,targetport):
        super(UavThread,self).__init__()
        #接受无人机端口
        uav_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        uav_recv_socket.bind(("", recvport))
        self.sock = uav_recv_socket
        
        #发送无人机创建UDP套接字
        self.uav_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.uav_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #无人机 目标地址和端口
        self.uav_addr = (targetip, targetport)
        self.uavdata = Fight.Flight_Struct()
        self.locate=0.0
        self.mc=0.0
        self.v=0.0
        self.startTime = 0
        self.nextIndex=0
        self.lastIndex=0
        self.HeartbeatCheck = 0
        self.flightLength =0
        self.mqttclient =None
        self.history_id = 0
        self.fps = 0
        # self.startTime =time.time()
        # pod = Fight.Flight_Action()
        # data =pod.Unlock()
        # self.Send(message)
        


    def run(self):
        heartbeat =Fight.Flight_HeartBeat()
        comfirm =Fight.Course_Confirm()
        path=Fight.Flight_Course_Struct()
        pathquery=Fight.Flight_Course_Query()
        check=Fight.Flight_Manage()
        startTime =time.time()
        if not os.path.exists("./history"):
            os.mkdir('./history',755)
        f = open('./history/{}'.format(self.history_id), 'wb')
        # print("self.HeartbeatCheck "
        while True: 
            
            data, addr = self.sock.recvfrom(4096)      # buffer size is 4096 bytes
            ctypes.memmove(ctypes.addressof(heartbeat), data, ctypes.sizeof(heartbeat))
            if(heartbeat.cmd == 0x08):
                print(" get heart beat ")
                # self.HeartbeatCheck =1
            elif(heartbeat.cmd == 0x05 and heartbeat.s_cmd == 0x22):
                print("update route")
                ctypes.memmove(ctypes.addressof(comfirm), data, ctypes.sizeof(comfirm))
                # self.nextIndex  = struct.unpack('<H',data[5:7])
                self.nextIndex  =  comfirm.next
                print("path comfirm",data.hex())
                print("update route index ",comfirm.next)
                if self.nextIndex ==  self.flightLength +1:
                    print('-------------航线上传完成--------------')
                    msg_dict ={'type':'loadsuccess'}
                    msg = json.dumps(msg_dict)
                    mqttclient.publish(TOPIC_INFO, msg)
                    code =check.Check()
                    uav.Send(code)
                    print("check send",code.hex())
                 
            
            elif(heartbeat.cmd == 0x05 and heartbeat.s_cmd == 0x41):
                ctypes.memmove(ctypes.addressof(pathquery), data, ctypes.sizeof(pathquery))
                # print("recieve query",pathquery.index)
                # print("check",data.hex())
                # print(data[6:24].hex())
                # print(flightPath[pathquery.index-1][6:24].hex())
                if pathquery.index <= self.flightLength:
                    if data[6:24] == flightPath[pathquery.index-1][6:24]  and data[28:30] == flightPath[pathquery.index-1][28:30]:
                        code =comfirm.PointComfirm(self.flightLength,pathquery.index)
                        uav.Send(code)
                        print("check send",code.hex())
                    else:
                        print("第 %d 个点不一致"%pathquery.index)

                    if pathquery.index == self.flightLength:
                        print("-------------航线装订成功--------------")
                        msg_dict ={'type':'loadchecksuccess'}
                        msg = json.dumps(msg_dict)
                        # print("msg:"+msg)
                        # print ('mqttclient ',mqttclient)
                        mqttclient.publish(TOPIC_INFO, msg)
                
                    
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
                
            elif(heartbeat.cmd == 0x10):
                # if  heartbeat.s_cmd == 0x10:
                #     self.fps += 1
                #     if time.time() +1 > fpstime:
                #         fpstime = time.time()
                if  startTime + 2 < time.time():
                    # print(data[0:15].hex() )
                    ctypes.memmove(ctypes.addressof(self.uavdata), data, ctypes.sizeof(self.uavdata))
                    # print(hex(self.uavdata.cmd))
                    # print(hex(self.uavdata.s_cmd))
                    # print(hex(self.uavdata.temp))
                    # print(hex(self.uavdata.eng))
                    #保存文件数据
                    f.write(data)

                    # print(self.uavdata.v/10)
                    # print(self.uavdata.a/10)
                    msg_dict ={'type':'drone','data': {
                    'temp':self.uavdata.temp,
                    'eng':self.uavdata.eng,
                    'v':self.uavdata.v/10,
                    'a':self.uavdata.a/10,
                    'offset_staus':self.uavdata.offset_staus,
                    'speed':self.uavdata.speed/100,
                    'lat': round(self.uavdata.lat/10000000,8),  #纬度
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
                    'HDOP':self.uavdata.HDOP,
                    'VDOP':self.uavdata.VDOP,
                    'SDOP':self.uavdata.SDOP,
                    'height_cm':self.uavdata.height_cm

                    }
                    }
                    msg = json.dumps(msg_dict)
                    
                    if uav.uavdata.staus &(1<<1):
                        self.mc = 1
                    else:
                        self.mc = 0
                    # print(self.mc)

                    r.set('lat',self.uavdata.lat/10000000)
                    r.set('lon',self.uavdata.lon/pow(10,7))
                    r.set('height',self.uavdata.height)
                    
                    # r.hset('drohearbeatthreadmps(msg_dict)
                    # print("msg:"+msg)
                    # print ('mqttclient ',mqttclient)
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
            # print ("%x "%(data))
            # print("Uav Sended :", str(len))
        except:
            print("Uav Sending Error!!!\n ")

# 组播组的IP和端口
MCAST_GRP = '226.0.0.80'
MCAST_PORT = 20002

#机场数据 处理数据
class AirportThread(threading.Thread):
    def __init__(self , ip ,port,rport):
        super(AirportThread,self).__init__()
        #接受机场数据端口
        print ("airport  :"+str(ip)+  "   " + str(port) + "   " + str(rport))

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
        self.airportdata = Fight.Airport_Receive()

    def run(self):
        
        while True:
            # print ("airport recv ---:")

            data, addr = self.sock.recvfrom(1024)      # buffer size is 4096 bytes
            ctypes.memmove(ctypes.addressof(self.airportdata), data, ctypes.sizeof(self.airportdata))
            # print('from '+str(addr))

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
            msg = json.dumps(msg_dict)
            # print("msg:"+msg)
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
            print("Airport Sended " + str(len))
        except:
            print("Airport Sending Error!!!\n")
            

#摄像头处理线程
class CameraThread(threading.Thread):
    def __init__(self , camip,camport):
        super(CameraThread,self).__init__()
        cam_recv_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  
        cam_recv_socket.bind(("", camport))
        self.sock = cam_recv_socket
        
        #发送无人机创建UDP套接字
        self.cam_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.cam_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        #无人机 目标地址和端口
        self.cam_addr = (camip, camport)
        # self.Send(message)

    def run(self):
        cam_data = Fight.Pod_Receive()
        while True:
            data, addr = self.sock.recvfrom(4096)      # buffer size is 4096 bytes
            # print('from '+str(addr))
            ctypes.memmove(ctypes.addressof(cam_data), data, ctypes.sizeof(cam_data))
            # print ("cam recv :",cam_data.type)
            if cam_data.type == 0x04:
        
                msg_dict ={'type':'monitor','data': {
                    'lon':round(cam_data.lon,8),  #target经度
                    'lat':round(cam_data.lat,8),    #target纬度
                    'target_height': cam_data.target_height,  #target高度
                    'tf_total': cam_data.tf_total/10,   #TF卡总容量
                    'tf_usage':cam_data.tf_usage,   #TF卡使用容量百分比 0-100%  
                }
                }
                msg = json.dumps(msg_dict)
                # print(msg)
                # result = mqttclient.publish(TOPIC_INFO, msg)
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
        
# 无人机ip  发送端口 接收端口 载荷ip  载荷 端口
#  192.168.8.200  14551 14550 192.168.2.300 4098
if __name__ == "__main__":    
    parser = argparse.ArgumentParser()
    # 添加位置参数
    parser.add_argument("ip", help="uav ip here")
    parser.add_argument("port", help="uav port...", type=int)
    parser.add_argument("r_port", help="uav port...", type=int)
    parser.add_argument("monitor_ip", help="cam ip here")
    parser.add_argument("monitor_port", help="cam port...", type=int)
    parser.add_argument("airport_ip", help="airport ip here")
    parser.add_argument("airport_port", help="airport port...", type=int)
    parser.add_argument("airport_rport", help="airport recvport...", type=int)
    parser.add_argument("camera_url", help="camera url ...")

    # parser.add_argument("steam_url", help="uav camera video steam")

    args = parser.parse_args()

    print('UAV Connect' + args.ip + " "+ str(args.port) +" "+ str(args.r_port) + " Camera :"+args.monitor_ip + " "+str(args.monitor_port) +
          " Airport :"+args.airport_ip + " "+str(args.airport_port) +" "+str(args.airport_rport)+"  "+str(args.camera_url))

    #发送无人机创建UDP套接字
    # uav_udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # uav_udp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    
    # # #无人机 目标地址和端口
    # target_addr = (args.ip, args.port)
    # SendData(uav_udp_socket,target_addr,message)

    # mqttclient = connect_mqtt()
    # yolov8_obj = yolo.yolov8()

    camera_url = args.camera_url

    print ("uav thread")
    global uav
    uav = UavThread(args.r_port,args.ip,args.port)
    uav.start()

    print ("camera thread")
    global cam
    cam = CameraThread(args.monitor_ip,args.monitor_port)
    cam.start()
    #cam.Send(message)
    # ReceiveData(uav_recv_socket)

    #机场连接
    print ("airport thread")
    global airport
    airport = AirportThread(args.airport_ip,args.airport_port,args.airport_rport)
    airport.start()

    # 心跳发送
    print ("Hearbeat thread")
    global hearbeatthread
    hearbeatthread = HearbeatThread()
    hearbeatthread.start()

    loop = asyncio.get_event_loop()

    loop.add_signal_handler(signal.SIGINT, ask_exit)
    loop.add_signal_handler(signal.SIGTERM, ask_exit)

    host = '127.0.0.1'


    loop.run_until_complete(mqttconnect(host))

    
    # uav.join()
    # cam.join()
    
    # airport.join()
    print ("after camera")
    loop.stop()
    loop.close()
    # uav_udp_socket.close()