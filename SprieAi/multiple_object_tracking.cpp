#include <iostream>
#include <string>
// 包含SpireCV SDK头文件
#include <opencv2/highgui/highgui.hpp>
#include <sv_world.h>
#include "mqtt/client.h"
#include "mqtt/callback.h"
#define SNAP_TIME 5
const std::string TOPIC("ai");
const std::string CLIENT_ID("33f1c750-01a6-4a26-9057-6a5adf0f80f5");
const int QOS = 1;
int HISTORY_ID =-1;
int AI_ID =-1;

int WHILE_LOOP =1;

using namespace std;
class user_callback : public virtual mqtt::callback
{
  void connection_lost(const std::string& cause) override {
    std::cout << "\nConnection lost" << std::endl;
    if (!cause.empty())
    std::cout << "\tcause: " << cause << std::endl;
    }
    void message_arrived(mqtt::const_message_ptr msg) override{
      if(msg->get_payload().find("fly_over") && HISTORY_ID > 0){
        WHILE_LOOP = 0;
      }

      std::cout << "\n\t[Delivery complete for token: "<< msg->get_payload()<<endl;
    }

    // void delivery_complete(mqtt::delivery_token_ptr tok) override {
    //   std::cout << "\n\t[Delivery complete for token: "
    //   << (tok ? tok->get_message_id() : -1) << "]" << std::endl;
    // }
    
  public:
};
// rtsp    filepath    historyid  ai_id on/off save/nosave
//rtsp:// path  32(history_id) 30 on(on:display/none:(nodisplay ) save(save/nosave)
int main(int argc, char *argv[]) {
  if(argc < 4){
      std::cout << "argc < 5 :rtsp:// path  32(history_id) on(on:display/none:(nodisplay ) save(save/nosave)" << std::endl;
      return 0;
  }

  mqtt::client client("tcp://127.0.0.1:1883", CLIENT_ID);


  user_callback cb;
  client.set_callback(cb);

  bool needShow=false;
  if (argc >=4 && strcmp(argv[5], "on") == 0)
    needShow = true;
  
  bool needSave=false;
  if (argc >=5 && strcmp(argv[6], "save") == 0)
    needSave = true;
  
  HISTORY_ID =atoi(argv[3]);
  AI_ID =atoi(argv[4]);

  
  mqtt::connect_options connOpts;
  connOpts.set_keep_alive_interval(20);
  connOpts.set_clean_session(true);
  
try {
  std::cout << "\nConnecting..." << std::endl;
  client.connect(connOpts);
  std::cout << "...OK" << std::endl;
  client.subscribe("fly_control",1);
  

  char s_buf[128];
  char send_buf[512];
  string url(argv[1]); 
  string pathname = argv[2];
  
  
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
  
  // 打开摄像头
  sv::Camera cap;
  cap.setWH(mot.image_width, mot.image_height);
  cap.setFps(30);
  
  std::cout << "url:"<<url<<endl;

  cap.setRtspUrl(url);
  // cap.setRtspUrl("rtsp://192.168.100.160:8554/0");
  // cap.setRtspUrl("rtsp://127.0.0.1:5554/live/test");

  cap.open(sv::CameraType::RTSP);  // CameraID 0

  // if(!cap.isOpened()){

  // }

  sv::VideoWriter vw;
  // 设置保存路径"/home/amov/Videos"，保存图像尺寸（640，480），帧频25Hz，同步保存检测结果（.svj）

  if(needSave){
    vw.setup(pathname.c_str(), cv::Size(cod.image_width, cod.image_height), 25, true);
  }
  time_t t = time(NULL);
  double lastTime = 0;


  vector<int> compression_params; //vector that stores the compression parameters of the image
  // 实例化OpenCV的Mat类，用于内存单帧图像
  cv::Mat img;
  int frame_id = 0;
  while (WHILE_LOOP == 1)
  {
    // 实例化SpireCV的 单帧检测结果 接口类 TargetsInFrame
    sv::TargetsInFrame tgts(frame_id++);
    // 读取一帧图像到img
    cap.read(img);
    cv::resize(img, img, cv::Size(mot.image_width, mot.image_height));
    // client.publish(pubmsg);


    // 执行通用目标检测
    mot.track(img, tgts);
    // 可视化检测结果，叠加到img上
    sv::drawTargetsInFrame(img, tgts);

    time(&t); 
    if(tgts.targets.size()> 0  && lastTime +SNAP_TIME < t){
      lastTime = t;
      strftime(s_buf, 64, "snap_%Y-%m-%d_%H-%M-%S.jpg", std::localtime(&t));
      std::string name = std::string(s_buf);
      std::string topathname = pathname+"/"+name;
      cv::imwrite(topathname, img,compression_params);

      if(HISTORY_ID >= 0){
        sprintf(send_buf, "{\"type\":%d,\"platform\":1,\"history_id\":%d,\"image\":\"%s/%s\"}", tgts.targets[0].category_id,HISTORY_ID,pathname.c_str(),s_buf);
      }        
      else if(AI_ID >=0 ){
        sprintf(send_buf, "{\"type\":%d,\"platform\":2,\"history_id\":%d,\"image\":\"%s/%s\"}", tgts.targets[0].category_id,AI_ID,pathname.c_str(),s_buf);
      }
        std::cout << "send:"<<send_buf << std::endl;

      auto pubmsg = mqtt::make_message(TOPIC,send_buf);
      pubmsg->set_qos(QOS);
      client.publish(pubmsg);     // 确保与mqtt broker server建立连接之后再publish!!!
    }
    //save video
    if(needSave){
      vw.write(img);
    }

    // 显示检测结果img
    // cv2.namedWindow("消息类型", cv2.WND_PROP_FULLSCREEN)
    // cv.setWindowProperty("foo", cv.WND_PROP_FULLSCREEN, cv.WINDOW_FULLSCREEN)
    if(needShow){
      cv::imshow("消息类型", img);
    }

    cv::waitKey(10);
  }

  vw.release();
  cap.release();
  // Disconnect
  std::cout << "\nDisconnecting..." << std::endl;
  client.disconnect();
  std::cout << "...OK" << std::endl;
  }
  catch (const mqtt::persistence_exception& exc) {
  std::cerr << "Persistence Error: " << exc.what() << " ["
  << exc.get_reason_code() << "]" << std::endl;
  return 1;
  }
  catch (const mqtt::exception& exc) {
  std::cerr << exc.what() << std::endl;
  return 1;
  }

  std::cout << "...finished" << std::endl;

  std::cout << "over" << std::endl;
  return 0;
}
