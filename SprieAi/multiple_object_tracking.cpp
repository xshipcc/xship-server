#include <iostream>
#include <string>
#include<iostream>  

// 包含SpireCV SDK头文件
#include <sv_world.h>

using namespace std;


#include "mqtt_client.hpp"
#define SNAP_TIME 5

using namespace std;
void on_cloud_message(const string& data)
{
    // 接收数据
    std::cout<<"received data is: "<<data<<std::endl;
}

template <typename T>
bool contains(vector<T> vec, const T & elem)
{
    bool result = false;
    if( find(vec.begin(), vec.end(), elem) != vec.end() )
    {
        result = true;
    }
    return result;
}

int main(int argc, char *argv[]) {
   if(argc < 5)
    {
      printf("CMD rtsp:// SavePath historyid on/off \n");
      return 0;
    }
  cloud::mqtt_client g_client("127.0.0.1:1883");    // 定义一个mqtt客户端
  std::cout << "[CLOUD] listen starting"<<std::endl;
  g_client.set_message_handler(on_cloud_message);     // 开启mqtt clinet监听消息，消息处理函数为on_cloud_message
//   g_client.send("online...");     // 确保与mqtt broker server建立连接之后再publish!!!
  // 实例化
  sv::CommonObjectDetector cod;
  // 手动导入相机参数，如果使用Amov的G1等吊舱或相机，则可以忽略该步骤，将自动下载相机参数文件
  cod.loadCameraParams(sv::get_home() + "/SpireCV/confs/calib_webcam_1920x1080.yaml");
  cod.loadAlgorithmParams(sv::get_home() + "/SpireCV/confs/sv_algorithm_params.json");
  sv::MultipleObjectTracker mot;
  // 手动导入相机参数，如果使用Amov的G1等吊舱或相机，则可以忽略该步骤，将自动下载相机参数文件
  mot.loadCameraParams(sv::get_home() + "/SpireCV/confs/calib_webcam_1920x1080.yaml");
  mot.loadAlgorithmParams(sv::get_home() + "/SpireCV/confs/sv_algorithm_params.json");
  mot.init(&cod);
  
	string strdir = argv[2];
  
  // if (access(strdir.c_str(), 0) == -1)//返回值为-1，表示不存在
	// {
	// 	printf("不存在,创建一个\n");
	// 	int i = mkdir(strdir.c_str());
	// }
  // 打开摄像头
  sv::Camera cap;
  cap.setWH(mot.image_width, mot.image_height);
  cap.setFps(30);
  cap.setRtspUrl(argv[1]);
  // cap.setRtspUrl("rtsp://192.168.100.160:8554/0");
  // cap.setRtspUrl("rtsp://127.0.0.1:5554/live/test");

  cap.open(sv::CameraType::RTSP);  // CameraID 0
  // 实例化OpenCV的Mat类，用于内存单帧图像
  cv::Mat img;
  int frame_id = 0;


  char s_buf[128];
  char send_buf[512];

  // 实例化视频保存类
  sv::VideoWriter vw;
  // 设置保存路径"/home/amov/Videos"，保存图像尺寸（640，480），帧频25Hz，同步保存检测结果（.svj）
  sprintf(send_buf, "%s/",argv[2]);
  vw.setup(send_buf, cv::Size(cod.image_width, cod.image_height), 25, true);


  bool needShow=false;

  if (strcmp(argv[4], "on") == 0)
    needShow = true;
  
  std::string pathname = argv[2];
  std::string filename;


  vector<int> trackers; //vector that stores the compression parameters of the image

  vector<int> compression_params; //vector that stores the compression parameters of the image

  // compression_params.push_back(CV_IMWRITE_JPEG_QUALITY); //specify the compression technique

  // compression_params.push_back(98); //specify the compression quality
  time_t t = time(NULL);
  double lastTime = 0;
  bool hasNew=false;
  int catatype;

  while (1)
  {
    // 实例化SpireCV的 单帧检测结果 接口类 TargetsInFrame
    sv::TargetsInFrame tgts(frame_id++);
    // 读取一帧图像到img
    cap.read(img);
    cv::resize(img, img, cv::Size(mot.image_width, mot.image_height));

    // 执行通用目标检测
    mot.track(img, tgts);
    // 可视化检测结果，叠加到img上
    sv::drawTargetsInFrame(img, tgts);
    

    // 同步保存视频流 和 检测结果信息
    vw.write(img);
    
    //found new tracker , to save to path /javodata/upload/ai/2023-11-30/
    //javodata/upload/ai/2023-11-30/uav_history_id/snap/
    //javodata/upload/ai/2023-11-30/uav_history_id/record/
    //javodata/upload/ai/2023-11-30/uav_history_id/uav/
    // printf("video  %d \n",vw.isRunning());
    hasNew =false;
    for (int i=0; i<tgts.targets.size(); i++)
    {
      if(!contains(trackers, tgts.targets[i].tracked_id))
      {
        trackers.push_back(tgts.targets[i].tracked_id);
        hasNew = true;
        catatype = tgts.targets[i].category_id;
        break;
        
      }

    }
    //tm t = *std::localtime(&t);
    time(&t); 
    if(hasNew && lastTime +SNAP_TIME < t){
      lastTime = t;
      strftime(s_buf, 64, "snap_%Y-%m-%d_%H-%M-%S.jpg", std::localtime(&t));
      printf("snapshot  %s \n" ,s_buf);
      std::string name = std::string(s_buf);
      std::string topathname = pathname+"/"+name;
      cv::imwrite(topathname, img,compression_params);
      sprintf(send_buf, "{\"type\":%d,\"history_id\":%s,\"image\":\"uploads/%s\"}", catatype,argv[3],s_buf);

      g_client.send(send_buf);     // 确保与mqtt broker server建立连接之后再publish!!!
    }
    hasNew = false;
    


    // 显示检测结果img
    if(needShow)
       cv::imshow("img", img);

    // 显示检测结果img
    cv::imshow("img", img);
    cv::waitKey(10);
  }

  return 0;
}
