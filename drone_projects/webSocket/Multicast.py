# coding:utf8

from twisted.internet.protocol import DatagramProtocol
from twisted.internet import reactor

multicast_ip = '226.0.0.80'
port = 6091
toport =8002

class Multicast(DatagramProtocol):
    def startProtocol(self):
        '''
        加入组播（必须重新）
        :return: 
        '''
        self.transport.setTTL(5) # 设置多播数据包的生存时间
        self.transport.joinGroup(multicast_ip)
        self.transport.write('Notify'.encode('utf8'),(multicast_ip,toport))

    def datagramReceived(self, datagram: bytes, addr):
        '''
        接收到组播发送的数据
        :param datagram: 
        :param addr: 
        :return: 
        '''
        print('Datagram %s received from %s '%(repr(datagram.hex()),repr(addr)))
        # if datagram.decode('utf8') == 'Notify':
        #     self.transport.write('Acknowlege'.encode('utf8'),(multicast_ip,toport))

    def closeConnection(self):
        '''
        自定义函数，离开组播时调用
        :return: 
        '''
        self.transport.leaveGroup()

reactor.listenMulticast(port,Multicast(),listenMultiple=True)
reactor.run()
