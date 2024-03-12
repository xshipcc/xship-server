# main.py
import time
import serial
import threading
import MulticastDataReceiver as UDPWorker


# #摇杆线程
class JoystickThread(threading.Thread):
    def __init__(self,tty):
        super(JoystickThread,self).__init__()
        self.ser = serial.Serial(tty.strip(), 115200)   # 'COM1'为串口名称，根据实际情况修改；9600为波特率，也可以根据设备要求调整
        self.isStop = False


    def Stop(self):
        self.isStop = True

    def Next(self):
        self.isStop = False

    def run(self):
        while self.isStop == False:           
            data  = self.ser.read(size=32)
            print('com from '+data.hex())
    
def main():
    print ("JoystickThread")
    global joyThread
    joyThread = JoystickThread("/dev/ttyUSB0")
    joyThread.start()

    try:
        while True:
            time.sleep(2)
            pass
    except KeyboardInterrupt:
        print("sss")

if __name__ == "__main__":
    main()
