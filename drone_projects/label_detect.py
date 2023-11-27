import os
import signal
import subprocess
import cv2
import redis
from ultralytics import YOLO
from collections import defaultdict
from PIL import Image
import hyperlpr3 as lpr3
from gmqtt import Client as MQTTClient
import asyncio
import json
import datetime

yolov8x_moedl = '/javodata/drone_projects/file/best.pt'
model = YOLO(yolov8x_moedl) 

# cap = cv2.VideoCapture("rtsp://192.168.8.160:554/live/track0")
cap = cv2.VideoCapture("/javodata/drone_projects/file/car5.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))
fNUMS = cap.get(cv2.CAP_PROP_FRAME_COUNT)

fourcc = cv2.VideoWriter_fourcc(*'mp4v')
videoWriter = cv2.VideoWriter("/javodata/drone_projects/out/1.mp4", fourcc, fps, size)

obejcts= {
  '0': {'name':'people','color':[0, 161, 255]},   #人 橙色
  '1': {'name':'car','color':[139,0,0]},          #车 蓝色
  '2': {'name':'bicycle','color':[170,255,127]},  #自行车 绿色
  '3': {'name':'bus','color':[42,42,165]},        #巴士 棕色
  '4': {'name':'van','color':[128,0,128]},        #面包车 紫色     
  '5': {'name':'truck','color':[139,139,0]},      #卡车 深青色
  '6': {'name':'tricycle','color':[225,215,0]},   #三轮车 金色
  '7': {'name':'motor','color':[0,0,0]},          #摩托车 黑色
  '8': {'name':'smoke','color':[144,128,112]},    #烟雾 灰色
  '9': {'name':'fire','color':[0,0,255]}          #火焰 红色
}


BROKER = '127.0.0.1'
PORT = 1883
TOPIC_INFO = "info"
TOPIC_ALERT = "ai"
TOPIC_CTRL = "control"

CLIENT_ID = f'pushuav_ai'
USERNAME = ''
PASSWORD = ''

mqttclient=None

r = redis.Redis(host='127.0.0.1',port=6379,db=0)

# 创建FFmpeg命令行参数
ffmpeg_cmd = ['ffmpeg',
              '-y',  # 覆盖已存在的文件
              '-f', 'rawvideo',
              '-pixel_format', 'bgr24',
              '-video_size', '960x540',
              '-i', '-',  # 从标准输入读取数据
              '-c:v', 'libx264', #使用x264编码器
              '-preset', 'ultrafast',   #使用ultrafast预设，以获得更快的编码速度
              '-tune', 'zerolatency',#零延迟
              '-pix_fmt', 'yuv420p',
              '-f', 'flv',
              'rtmp://127.0.0.1/live/test'
            ]



# ffmepg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)

async def on_message(client, topic, payload, qos, properties):
    print(payload)

    
def on_connect(client, flags, rc, properties):
    print('mqtt Connected')

def on_subscribe(client, mid, qos, properties):
    print('mqtt SUBSCRIBED')

def on_disconnect(client, packet, exc=None):
    print('mqtt Disconnected')

def ask_exit(*args):
    STOP.set()

STOP = asyncio.Event()

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


    # await STOP.wait()
    # await mqttclient.disconnect()


loop = asyncio.get_event_loop()

loop.add_signal_handler(signal.SIGINT, ask_exit)
loop.add_signal_handler(signal.SIGTERM, ask_exit)

host = '127.0.0.1'


loop.run_until_complete(mqttconnect(host))

STOP = asyncio.Event()

def box_label(image, box, label='', color=(128, 128, 128), txt_color=(255, 255, 255)):
    #得到目标矩形框的左上角和右下角坐标
    p1, p2 = (int(box[0]), int(box[1])), (int(box[2]), int(box[3]))
    #绘制矩形框
    cv2.rectangle(image, p1, p2, color, thickness=1, lineType=cv2.LINE_AA)
    if label:
        #得到要书写的文本的宽和长，用于给文本绘制背景色
        w, h = cv2.getTextSize(label, 0, fontScale=2/3, thickness=1)[0]  
        #确保显示的文本不会超出图片范围
        outside = p1[1] - h >= 3
        p2 = p1[0] + w, p1[1] - h - 3 if outside else p1[1] + h + 3
        cv2.rectangle(image, p1, p2, color, -1, cv2.LINE_AA)     #填充颜色
        #书写文本
        cv2.putText(image,
                label, (p1[0], p1[1] - 2 if outside else p1[1] + h + 2),
                0,
                2 / 3,
                txt_color,
                thickness=1,
                lineType=cv2.LINE_AA)
        
# track_history用于保存目标ID，以及它在各帧的目标位置坐标，这些坐标是按先后顺序存储的
# track_history = defaultdict(lambda: [])
track_history = {}
#车辆的计数变量
vehicle_in = 0
vehicle_out = 0
catrher = lpr3.LicensePlateCatcher()
fps =10
#1、推送一个视频流进行直播
#2、推送报警 识别Tracker的 第一个报警图片，车，人，时间，坐标（计算摄像头的识别位置的坐标）
#3、保存视频到一个历史播放文件。提供播放

famecheck =0
num =0
#视频帧循环
while cap.isOpened():
    #读取一帧图像
    success, frame = cap.read()
    if success:
        #在帧上运行YOLOv8跟踪，persist为True表示保留跟踪信息，conf为0.3表示只检测置信值大于0.3的目标
        results = model.track(frame,conf=0.3, persist=True)
        print('len ',len(results))

        #得到该帧的各个目标的ID
        if results[0].boxes.id is not None:
            track_ids = results[0].boxes.id.int().cpu().tolist()
            #遍历该帧的所有目标  
            famecheck +=1
            for track_id, box in zip(track_ids, results[0].boxes.data):
                #tracker 保存 识别对象。
                # if box[-1] == 1 and famecheck%20 ==0:   #目标为小汽车
                    #    if boxes[0] is not None:
                            # xmin = int(boxes[0].xyxy[0,0])
                            # ymin = int(boxes[0].xyxy[0,1])
                            # xmax = int(boxes[0].xyxy[0,2])
                            # ymax = int(boxes[0].xyxy[0,3])
                            
                            # # img = Image.fromarray(frame)
                            # # crop_image = img.crop((xmin, ymin, xmax,ymax))
                            # print(xmin,xmax ,  ymin, ymax )
                            # if( xmax > xmin and ymax > ymin):
                            #     print(catrher(frame[xmin:ymin, xmax:ymax]))
                #绘制该目标的矩形框
                
                #得到该目标矩形框的中心点坐标(x, y)
                x1, y1, x2, y2 = box[:4]
                x = (x1+x2)/2
                y = (y1+y2)/2
                # print("coord",x1)
                # #提取出该ID的以前所有帧的目标坐标，当该ID是第一次出现时，则创建该ID的字典
                foundtrack =track_history.get(track_id)
                
                if foundtrack == None:

                    #alert 
                    track_history[track_id] = 0
                else:
                    track_history[track_id] += 1

                print(str(box)+":"+str(track_history[track_id]))
                if track_history[track_id]== 20:
                    # response = results[0]
                    # boxes = response.boxes
                    
                    # while index < len(boxes):
                    # xmin = float(boxes[index].xyxy[0,0])
                    # ymin = float(boxes[index].xyxy[0,1])
                    # xmax = float(boxes[index].xyxy[0,2])
                    # ymax = float(boxes[index].xyxy[0,3])
                    xmin = float(box[0])
                    ymin = float(box[1])
                    xmax = float(box[2])
                    ymax = float(box[3])
                    img = Image.fromarray(frame)
                    crop_image = img.crop((xmin, ymin, xmax,ymax))
                    now = datetime.datetime.now()
                    
                    path = "uploads/ai/{}/".format(now.strftime('%Y-%m-%d'))
                    if not os.path.lexists(path): 
                        os.makedirs(path)
		# Name      string  `db:"name"`       // 报警标题
		# Image     string  `db:"image"`      // 报警截图
		# Type      int64   `db:"type"`       // 消息类型:0-发现人员 1-車輛 2-入侵 3-烟火 4-
		# Code      string  `db:"code"`       // 系统分类二级类别
		# Level     int64   `db:"level"`      // 预警等级
		# Count     int64   `db:"count"`      // 报警数量
		# Platform  int64   `db:"platform"`   // 使用平台：0-全部 1-飞机 2-摄像头;3-机库;4-AI
		# Lat       float64 `db:"lat"`        // 经度
		# Lon       float64 `db:"lon"`        // 纬度
		# Alt       float64 `db:"alt"`        // 高度
		# StartTime string  `db:"start_time"` // 开始时间
		# EndTime   string  `db:"end_time"`   // 结束时间
		# Note      string  `db:"note"`       // 备注
		# Confirm   int64   `db:"confirm"`    // 报警确认
                    filename = "{}{}-{}.jpg".format(path,now.strftime('%H:%M:%S'),track_id)
                    crop_image.save(filename)
                    msg_dict ={"name":"sss",
                                "type":curbox,
                                "lat":r.get('lat'),
                                "lon":r.get('lon'),
                                "alt":r.get('height'),
                                "history_id":3,
                                "start_time":now.strftime('%Y-%m-%d %H:%M:%S'),
                                "image":filename}
                    msg = json.dumps(msg_dict)
                    print(mqttclient )
                    mqttclient.publish(TOPIC_ALERT, msg)
                        # index +=1
                #draw 
                curbox = int(box[-1])
                box_label(frame, box, '#'+str(track_id)+obejcts[str(curbox)]['name'], (obejcts[str(curbox)]["color"][0],
                                                                                    obejcts[str(curbox)]["color"][1],
                                                                                    obejcts[str(curbox)]["color"][2]))
                # track.append((float(x), float(y)))  #追加当前目标ID的坐标
                #只有当track中包括两帧以上的情况时，才能够比较前后坐标的先后位置关系
                # if len(track) > 1:
                #     _, h = track[-2]  #提取前一帧的目标纵坐标
                #     #我们设基准线为纵坐标是size[1]-400的水平线
                #     #当前一帧在基准线的上面，当前帧在基准线的下面时，说明该车是从上往下运行
                #     if h < size[1]-400 and y >= size[1]-400:
                #         vehicle_out +=1      #out计数加1
                #     #当前一帧在基准线的下面，当前帧在基准线的上面时，说明该车是从下往上运行
                #     if h > size[1]-400 and y <= size[1]-400:
                #         vehicle_in +=1       #in计数加1

            # elif box[-1] == 0:   #目标为人
            #     box_label(frame, box, '#'+str(track_id)+' bus', (100, 21, 55))
                

            # elif box[-1] == 2:   #目标为人
            #     box_label(frame, box, '#'+str(track_id)+' bus', (100, 21, 55))
                
                

            # elif box[-1] == 3:   #目标为巴士
            #     box_label(frame, box, '#'+str(track_id)+' bus', (67, 161, 255))
                
            #     x1, y1, x2, y2 = box[:4]
            #     x = (x1+x2)/2
            #     y = (y1+y2)/2
            #     track = track_history[track_id]
            #     track.append((float(x), float(y)))  # x, y center point
            #     if len(track) > 1:
            #         _, h = track[-2]
            #         if h < size[1]-400 and y >= size[1]-400:
            #             vehicle_out +=1
            #         if h > size[1]-400 and y <= size[1]-400:
            #             vehicle_in +=1 
               
            # elif box[-1] == 5:   #目标为卡车
            #     box_label(frame, box, '#'+str(track_id)+' truck', (19, 222, 24))
                
            #     x1, y1, x2, y2 = box[:4]
            #     x = (x1+x2)/2
            #     y = (y1+y2)/2
            #     track = track_history[track_id]
            #     track.append((float(x), float(y)))  # x, y center point
                
              
            # elif box[-1] == 3:   #目标为摩托车
            #     box_label(frame, box,'#'+str(track_id)+' motor', (186, 55, 2))
                
            #     x1, y1, x2, y2 = box[:4]
            #     x = (x1+x2)/2
            #     y = (y1+y2)/2
            #     track = track_history[track_id]
            #     track.append((float(x), float(y)))  # x, y center point
            #     if len(track) > 1:
            #         _, h = track[-2]
            #         if h < size[1]-400 and y >= size[1]-400:
            #             vehicle_out +=1
            #         if h > size[1]-400 and y <= size[1]-400:
            #             vehicle_in +=1 
        # #绘制基准线
        # cv2.line(frame, (30,size[1]-400), (size[0]-30,size[1]-400), color=(25, 33, 189), thickness=2, lineType=4)
        # #实时显示进、出车辆的数量
        # cv2.putText(frame, 'in: '+str(vehicle_in), (595, size[1]-410),
        #         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        # cv2.putText(frame, 'out: '+str(vehicle_out), (573, size[1]-370),
        #         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
 
        # cv2.putText(frame, "https://blog.csdn.net/zhaocj", (25, 50),
        #         cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
            annotated_frame = results[0].plot()

        #     ffmepg_process.stdin.write(annotated_frame.tobytes())
        # else:
        #     ffmepg_process.stdin.write(frame)

        cv2.imshow("YOLOv8 Tracking", frame)  #显示标记好的当前帧图像
        videoWriter.write(frame)  #写入保存
     
        if cv2.waitKey(1) & 0xFF == ord("q"):   #'q'按下时，终止运行
            break
 
    else:  #视频播放结束时退出循环
        break
 
#释放视频捕捉对象，并关闭显示窗口
cap.release()
videoWriter.release()
cv2.destroyAllWindows()