import socket
 
HOST = '192.168.2.200'
PORT = 14550
 
sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 
data = 'hello'
 
while data:
    sk.sendto(data.encode(), (HOST, PORT))
   
    data, addr = sk.recvfrom(1024)
    print("Recv Data:%s", data)
    # data = raw_input('Please message:\n')
 
sk.close()
 