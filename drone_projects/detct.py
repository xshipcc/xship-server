import cv2
from ultralytics import YOLO
import ffmpeg 
import subprocess
from yolov5.models.yolo import Model
from yolov5.models.experimental import attempt_download
import torch
import cv2
import torch
import time
import numpy as np
from PIL import Image

# 模型加载权重
yolov8x_moedl1 = 'file/car.pt'
# yolov8x_moedl = 'model/yolov8n.pt'
modelcar = YOLO(yolov8x_moedl1) 
yolov8x_moedl2 = 'file/best.pt'
# yolov8x_moedl = 'model/yolov8n.pt'
model2 = YOLO(yolov8x_moedl2) 
# yolov8x_moedl = 'file/carplate.pt'
# model = torch.hub.load('./yolov5/file','plate_best')
# model = torch.hub.load('yolov5', 'custom', path='file/plate_best.pt',source='local')

# model = Model('file/plate_best.pt')
# weights = 'file/plate_best.pt'
# model=attempt_download('weights')
#推流质量
# 设置编码参数

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



ffmepg_process = subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE)


# 视频路径
video_path = "/home/magix/uavserver/drone_projects/file/123.mp4"
cap = cv2.VideoCapture(video_path)
fourcc = cv2.VideoWriter_fourcc(*'MP4V')  # 其中*'MP4V'和 'M', 'P', '4', 'V'等效

fps = cap.get(cv2.CAP_PROP_FPS) #帧率
size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))) #自动获取视频大小
out = cv2.VideoWriter('file/output.avi', fourcc, fps, size)  #opencv好像只能导出avi格式
 
# 对视频中检测到目标画框标出来
while cap.isOpened():
    # Read a frame from the video
    success, frame = cap.read()
 
    if success:
        #在视频帧上运行YOLOv8推理
        resultscar = modelcar(frame)

        results2 = model2(frame)

        response = resultscar[0]
        boxes = response.boxes

        
        # cv2.imshow("YOLOv8 Inference", points)


        print('---->'+str(boxes[0].xyxy[0,0]))
        if boxes[0] is not None:
            xmin = float(boxes[0].xyxy[0,0])
            ymin = float(boxes[0].xyxy[0,1])
            xmax = float(boxes[0].xyxy[0,2])
            ymax = float(boxes[0].xyxy[0,3])
            img = Image.fromarray(frame)
            # img = frame.crop((xmin, ymin, xmax, ymax))  # 裁剪出车牌位置
            # img = img.resize((boxes[0].xywh[2], boxes[0].xywh[3]), Image.LANCZOS)
            # img = np.asarray(img)  # 转成array,变成24*94*3
            # cv2.imencode('.jpg', frame)[1].tofile(r"1111.jpg")
            crop_image = img.crop((xmin, ymin, xmax,ymax))
            track_ids = response.boxes.id.int().cpu().tolist()
            # 保存截取后的图片
            crop_image.save("crop_image{}.jpg".format(track_ids[0]))
            # dst = frame[xmin:ymin, xmax:ymax]
            # print('---->'+str(xmin))
            # cv2.imshow('crop_post',crop_image)
        
        # if boxes[0] is not None:
        #     xmin = rect[0]
        #     xmax = rect[0]+rect[2]
        #     ymin = rect[1]
        #     ymax = rect[1]+rect[3]

        # img = Image.fromarray(img)
        # img = frame.crop((xmin, ymin, xmax, ymax))  # 裁剪出车牌位置
        # img = img.resize((boxes[0].xywh[2], boxes[0].xywh[3]), Image.LANCZOS)
        # img = np.asarray(img)  # 转成array,变成24*94*3
        # cv2.imencode('.jpg', img)[1].tofile(r"1111.jpg")

        # cv2.imshow("YOLOv8 Inference", ddd)
        # annotated_frame = response.plot()
        # names = response.get('names')
        # print('boxes'+str(names))

        # 在视频帧上可视化结果
        # annotated_frame = results[0].plot()

        # 储存每一帧
        # out.write(annotated_frame)
        # ffmepg_process.stdin.write(annotated_frame.tobytes())
        # 展示
        # sp = boxes[0].xyxy
        # print(str(sp))            #获取图像形状：返回【行数值，列数值】列表
        # sz1 = sp[0]                 #图像的高度（行 范围）
        # sz2 = sp[1]                 #图像的宽度（列 范围）
        #sz3 = sp[2]                #像素值由【RGB】三原色组成
        
        #你想对文件的操作
        # a=int(sz1/2-64) # x start
        # b=int(sz1/2+64) # x end
        # c=int(sz2/2-64) # y start
        # d=int(sz2/2+64) # y end
        # cropImg = frame[sp[0]:sp[1],sp[2]:sp[3]]   #裁剪图像
        # # cv2.imwrite(dest,cropImg)  #写入图像路径

        # cv2.imshow("YOLOv8 Inference", img)

        # Break the loop if 'q' is pressed
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break
    else:
        # Break the loop if the end of the video is reached
        break
 
# Release the video capture object and close the display window
# 释放资源
ffmepg_process.stdin.close()
ffmepg_process.wait()
cap.release()
out.release()
cv2.destroyAllWindows()
