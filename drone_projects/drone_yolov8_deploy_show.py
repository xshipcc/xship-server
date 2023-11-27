# coding:utf-8

import os
import time

import cv2
import argparse

from utils import image_gps, gps_utils, udp_utils
from multiprocessing import Process, Queue
from ultralytics import YOLO



class yolov8:
    def process(self, in_q, out_q):
        yolov8x_moedl = 'model/yolov8s.pt'
        model = YOLO(yolov8x_moedl)
        while True:
            if in_q.empty():
                # print('原始图像队列为空')
                time.sleep(0.5)
            else:
                frame = in_q.get()
                res = model(frame)
                response = res[0]
                boxes = response.boxes
                if boxes:
                    # print(response)
                    # print('!!!!!!!!')
                    # print(response.type())
                    # print('~~~~~~~')
                    # print(response.get('names'))
                    # print(response['names'])
                    # print('@@@@@@@@@')
                    # print(response.get('boxes'))
                    res_plotted = res[0].plot()
                    if not out_q.full():
                        out_q.put(res_plotted)


class gps:
    def get_info(self, gps_q):
        import serial
        '''
        while True:
            lat, lng, alt = gps_utils.get_lat_lng()
            gps_info = lat, lng, alt
            if not gps_q.full():
                gps_q.put(gps_info)
        '''

        def get_gps_data_temp(device, bote, flag):
            while True:
                gps_info = 25, 56, 12
                gps_q.put(gps_info)
                time.sleep(0.05)

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
                        # lat = '4124.8963'
                        # lon = '4124.8963'
                        # alt = '214.7'
                        # print("维度：" + lat, "经度：" + lon, "高程：" + alt)
                        if lat and lon and alt:
                            lat = nmea0183_to_dms(lat)
                            lon = nmea0183_to_dms(lon)
                            print("维度：" + str(lat), "经度：" + str(lon), "高程：" + str(alt) + '\n')
                            gps_info = lat, lon, alt
                            gps_q.put(gps_info)
                    # print("******")
                except serial.SerialException:
                    print('Error occurred')

        if __name__ == '__main__':
            get_gps_data_temp('COM5', 4800, '$GPGGA')


class file_process:
    def save(self, origin_file_q, dest_file_q):
        while True:
            if origin_file_q.empty():
                print('没有需要保存的文件')
                time.sleep(0.1)
            else:
                img_path, frame = origin_file_q.get()
                cv2.imwrite(img_path, frame)

            if dest_file_q.empty():
                print('没有需要保存的文件')
                time.sleep(0.1)
            else:
                img_path, frame = dest_file_q.get()
                cv2.imwrite(img_path, frame)


class web_play:
    def play(self):
        import cv2
        from flask import Flask, render_template, Response, make_response, request

        # 全局变量 共享的文件夹路径 可以根据需求更改
        DIRECTORY_PATH = 'file/detection'

        app = Flask(__name__)

        @app.after_request
        def after_request(response):
            """
            添加header解决跨域
            :param response:
            :return:
            """
            response.headers['Access-Control-Allow-Origin'] = '*'
            response.headers['Access-Control-Allow-Credentials'] = 'true'
            response.headers['Access-Control-Allow-Method'] = 'POST, GET, OPTIONS, DELETE, PATCH, PUT'
            response.headers['Access-Control-Allow-Headers'] = '*'
            return response

        def gen_frames_success():
            capture = cv2.VideoCapture('/home/geekplusa/ai/datasets/download/bilibili/无人机/videos/drone.mp4')
            while True:
                success, frame = capture.read()
                ret, buffer = cv2.imencode('.jpg', frame)
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        def gen_frames():
            while True:
                # success, frame = capture.read()
                frame = cv2.imread('temp.jpg')
                # print('~~~~~~~~~~~~~~~~~~~~~~~~~~~~' + str(frame))
                if frame is not None:
                    ret, buffer = cv2.imencode('.jpg', frame)
                    frame = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

        @app.route('/')
        def index():
            return render_template('index.html')

        @app.route('/video_feed')
        def video_feed():
            return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')


        #############################文件展示##############################
        # 获取文件信息的函数
        def get_files_data():
            files = []
            for i in os.listdir(DIRECTORY_PATH):
                if len(i.split(".")) == 1:  # 判断此文件是否为一个文件夹
                    continue

                # 拼接路径
                file_path = DIRECTORY_PATH + "/" + i
                name = i
                size = os.path.getsize(file_path)  # 获取文件大小
                ctime = time.localtime(os.path.getctime(file_path))  # 格式化创建当时的时间戳

                # 列表信息
                files.append({
                    "name": name,
                    "size": size,
                    "ctime": "{}年{}月{}日".format(ctime.tm_year, ctime.tm_mon, ctime.tm_mday),  # 拼接年月日信息
                })
            return files

        @app.route("/file")
        def file_show():
            """共享文件主页"""
            return render_template("file.html", files=get_files_data())

        @app.route("/download_file/<filename>")
        def file_content(filename):
            """下载文件的URL"""
            if filename in os.listdir(DIRECTORY_PATH):  # 如果需求下载文件存在
                # 发送文件 参数：文件夹路径，文件路径，文件名
                # return send_from_directory(os.path.join(DIRECTORY_PATH, filename), filename)
                image_data = open(os.path.join(DIRECTORY_PATH, filename), "rb").read()
                response = make_response(image_data)
                response.headers['Content-Type'] = 'image/png'
                return response
            else:
                # 否则返回错误页面
                return None  # render_template("download_error.html", filename=filename)


        if __name__ == '__main__':
            app.run(host='0.0.0.0', port=5009, debug=True)


def process_video(video, output, fps, save_flag, show_flag, save_origin_time_interval, save_det_time_interval):
    print('~~~~~~~~~~~开始处理逻辑～～～～～～～～～～～～')
    # 1. 读取摄像头
    cap = cv2.VideoCapture(video)

    # 2. 获取图像的属性（宽和高，）,并将其转换为整数
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = int(cap.get(cv2.CAP_PROP_FPS))

    # 3. 创建保存视频的对象，设置编码格式，帧率，图像的宽高等
    out = cv2.VideoWriter(output, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), frame_count,
                          (frame_width, frame_height))  # 保存视频
    num = 0
    t1_origin = time.time()
    t1_det = time.time()

    # 文件循环播放
    frame_counter = 0
    while True:
        num += 1
        # 4.获取视频中的每一帧图像
        ret, frame = cap.read()
        res_plotted = frame

        frame_counter += 1
        if frame_counter == int(cap.get(cv2.CAP_PROP_FRAME_COUNT)):
            frame_counter = 0
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        if ret:
            if not in_q.full():
                in_q.put(frame)
            if num % fps == 0:
                # cv2.imwrite('temp.jpg', frame)
                t2_origin = time.time()
                if t2_origin - t1_origin >= save_origin_time_interval:
                    origin_file_name = 'file/origin/orgin_{%s}_{%s}.jpg' % (str(num), time.strftime("%Y-%m-%d_%H:%M:%S"))
                    cv2.imwrite(origin_file_name, frame)

                    # origin_file = origin_file_name, frame
                    # if not origin_file_q.full():
                    #     origin_file_q.put(origin_file)

                    t1_origin = t2_origin
                if out_q.empty():
                    # print('检测结果队列为空')
                    res_plotted = frame
                else:
                    res_plotted = out_q.get()
                    t2_det = time.time()
                    if t2_det - t1_det >= save_det_time_interval:
                        det_img_path = 'file/detection/detection_{%s}_{%s}.jpg' % (str(num), time.strftime("%Y-%m-%d_%H:%M:%S"))
                        cv2.imwrite(det_img_path, res_plotted)

                        # det_file = det_img_path, res_plotted
                        # if not dest_file_q.full():
                        #     dest_file_q.put(det_file)

                        # 实时获取gps经纬度信息
                        # lat, lng = gps_utils.get_lat_lng()
                        # image_gps.add_gps_info_test(det_img_path, lat, lng)
                        if gps_q.empty():
                            print('gps信息队列为空')
                            lat, lon, alt = 25, 144, 144
                        else:
                            lat, lon, alt = gps_q.get()
                        # lat, lng = gps_utils.get_lat_lng()
                        image_gps.add_gps_info_test(det_img_path, lat, lon, alt)

                        t1_det = t2_det

                # cv2.flip(frame, 1, frame)
                # 5.将每一帧图像写入到输出文件中
                if save_flag:
                    out.write(res_plotted)  # 视频写入

                cv2.imwrite('temp.jpg', res_plotted)
                if show_flag:
                    cv2.namedWindow("output", cv2.WINDOW_NORMAL)
                    cv2.imshow('output', res_plotted)
                    if cv2.waitKey(5) & 0xFF == 27:
                        break
        else:
            break

        '''
        cv2.imwrite('temp.jpg', res_plotted)
        if show_flag:
            cv2.namedWindow("output", cv2.WINDOW_NORMAL)
            cv2.imshow('output', res_plotted)
            if cv2.waitKey(5) & 0xFF == 27:
                break
        '''

    # 6.释放资源
    cap.release()
    out.release()  # 资源释放
    cv2.destroyAllWindows()
    output_new = output[:-4] + '_output' + output[-4:]
    os.system('ffmpeg -i ' + output + ' ' + output_new)
    os.system('rm -rf ' + output)
    os.system('mv ' + output_new + ' ' + output)
    return None


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # 添加位置参数
    parser.add_argument("ip", help="uav ip here")
    parser.add_argument("port", help="uav port...", type=int)
    
    parser.add_argument("hangar_ip", help="uav ip here")
    parser.add_argument("hangar_port", help="uav port...", type=int)

    parser.add_argument("steam_url", help="uav camera video steam")

    parser.parse_args()

    #################yolov8模型相关，用于推理图片#################
    yolov8_obj = yolov8()
    # 保存原始视频帧
    in_q = Queue(30)
    # 保存检测后的视频帧
    out_q = Queue(30)
    yolov8_process = Process(target=yolov8_obj.process, args=(in_q, out_q))
    yolov8_process.start()

    ####################gps相关，用于获取经纬度信息#############暂时不用
    gps_obj = gps()
    # 保存gps信息
    gps_q = Queue(2)
    gps_process = Process(target=gps_obj.get_info, args=(gps_q,))
    gps_process.start()

    ###########################图片保存相关，用于保存图片########暂时不用
    file_obj = file_process()
    # 保存file信息
    origin_file_q = Queue(2)
    dest_file_q = Queue(2)
    file_process = Process(target=file_obj.save, args=(origin_file_q, dest_file_q))
    # file_process.start()

    ########################web展示相关，用于展示视频效果####################
    web_play_obj = web_play()
    web_play_process = Process(target=web_play_obj.play, args=( ))
    web_play_process.start()

    ########################控制siyi摄像头的舵机角度####################
    # 这里睡眠10秒，防止系统刚启动，不能操作摄像头
    time.sleep(10)
    udp_utils.main()


    # videos = 0
    # videos = "rtsp://192.168.10.188:554/user=admin&password=&channel=1&stream=0.sdp?real_stream"
    videos = "rtsp://127.0.0.1/live/test"
    # videos = 'file/drone.mp4'
    # videos = 0
    save_flag = True
    show_flag = True
    fps = 1
    # 5秒保存一次原始图片
    save_origin_time_interval = 5
    # 10秒保存一次推理后的图片
    save_det_time_interval = 3
    process_video(videos, 'file/out_{%s}.avi' % time.strftime("%Y-%m-%d_%H_%M"), fps, save_flag, show_flag, save_origin_time_interval, save_det_time_interval)
