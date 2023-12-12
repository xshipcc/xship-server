# main.py
import time
import MulticastDataReceiver as UDPWorker

def main():
    # 组播地址和端口
    multicast_group = '226.0.0.80'
    multicast_port = 20002

    dest_addr = '226.0.0.80'
    dest_port = 20001

    receiver = UDPWorker.MulticastDataReceiver(multicast_group, multicast_port, dest_addr, dest_port)
    receiver.start()

    try:
        while True:
            time.sleep(2)
            pass
    except KeyboardInterrupt:
        receiver.stop()

if __name__ == "__main__":
    main()
