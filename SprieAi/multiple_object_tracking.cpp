#include <iostream>
#include <string>
// 包含SpireCV SDK头文件
#include <sv_world.h>
#include "mqtt/client.h"
const std::string TOPIC("ai");
const std::string CLIENT_ID("33f1c750-01a6-4a26-9057-6a5adf0f80f5");
const int QOS = 1;

using namespace std;
class user_callback : public virtual mqtt::callback
{
  void connection_lost(const std::string& cause) override {
    std::cout << "\nConnection lost" << std::endl;
    if (!cause.empty())
    std::cout << "\tcause: " << cause << std::endl;
    }
    
    void delivery_complete(mqtt::delivery_token_ptr tok) override {
    std::cout << "\n\t[Delivery complete for token: "
    << (tok ? tok->get_message_id() : -1) << "]" << std::endl;
  }
  
  public:
};

int main(int argc, char *argv[]) {
  mqtt::client client("tcp://127.0.0.1:1883", CLIENT_ID);


  user_callback cb;
  client.set_callback(cb);
  
  mqtt::connect_options connOpts;
  connOpts.set_keep_alive_interval(20);
  connOpts.set_clean_session(true);
  std::cout << "...OK" << std::endl;
  
try {
  std::cout << "\nConnecting..." << std::endl;
  client.connect(connOpts);
  std::cout << "...OK" << std::endl;
  
  // First use a message pointer.
  
  std::cout << "\nSending message..." << std::endl;
  auto pubmsg = mqtt::make_message(TOPIC, "Hello World,This is a message...");
  pubmsg->set_qos(QOS);
  client.publish(pubmsg);
  std::cout << "...OK" << std::endl;
  

  // 实例化
  sv::CommonObjectDetector cod;
  // 手动导入相机参数，如果使用Amov的G1等吊舱或相机，则可以忽略该步骤，将自动下载相机参数文件
  cod.loadCameraParams(sv::get_home() + "/SpireCV/confs/calib_webcam_1280x720.yaml");
  cod.loadAlgorithmParams(sv::get_home() + "/SpireCV/confs/sv_algorithm_params.json");
  sv::MultipleObjectTracker mot;
  // 手动导入相机参数，如果使用Amov的G1等吊舱或相机，则可以忽略该步骤，将自动下载相机参数文件
  mot.loadCameraParams(sv::get_home() + "/SpireCV/confs/calib_webcam_1280x720.yaml");
  mot.loadAlgorithmParams(sv::get_home() + "/SpireCV/confs/sv_algorithm_params.json");
  mot.init(&cod);
  
  // 打开摄像头
  sv::Camera cap;
  cap.setWH(mot.image_width, mot.image_height);
  cap.setFps(30);
  cap.setRtspUrl("rtsp://127.0.0.1:5554/live/test");
  // cap.setRtspUrl("rtsp://192.168.100.160:8554/0");
  // cap.setRtspUrl("rtsp://127.0.0.1:5554/live/test");

  cap.open(sv::CameraType::RTSP);  // CameraID 0
  // 实例化OpenCV的Mat类，用于内存单帧图像
  cv::Mat img;
  int frame_id = 0;
  while (1)
  {
    // 实例化SpireCV的 单帧检测结果 接口类 TargetsInFrame
    sv::TargetsInFrame tgts(frame_id++);
    // 读取一帧图像到img
    cap.read(img);
    cv::resize(img, img, cv::Size(mot.image_width, mot.image_height));
  client.publish(pubmsg);

    // 执行通用目标检测
    mot.track(img, tgts);
    // 可视化检测结果，叠加到img上
    sv::drawTargetsInFrame(img, tgts);
    
    // 显示检测结果img
    cv::imshow("img", img);
    cv::waitKey(10);
  }
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

  return 0;
}
