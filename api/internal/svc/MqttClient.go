package svc

import (
	"fmt"

	mqtt "github.com/eclipse/paho.mqtt.golang"
)

type MqttClient struct {
	broker   string
	port     int
	clientID string
	userName string
	passWord string
	Company  string
	client   mqtt.Client
}

var connectHandler mqtt.OnConnectHandler = func(client mqtt.Client) {

	fmt.Println("Mqtt Server Connected \n ")
}

var connectLostHandler mqtt.ConnectionLostHandler = func(client mqtt.Client, err error) {
	fmt.Printf("Connect lost: %v\n", err)
}

func newMQTTClient(broker string, port int, clientID string, userName, passWord string) mqtt.Client {
	opts := mqtt.NewClientOptions()
	opts.AddBroker(fmt.Sprintf("tcp://%s:%d", broker, port))
	opts.SetClientID(clientID)
	opts.SetUsername(userName)
	opts.SetPassword(passWord)
	opts.OnConnect = connectHandler
	opts.OnConnectionLost = connectLostHandler

	client := mqtt.NewClient(opts)
	if token := client.Connect(); token.Wait() && token.Error() != nil {
		panic(token.Error())
	}
	return client
}

func NewMqttSubOption(broker string, port int, clientID string, userName, passWord string, comp string) *MqttClient {
	client := newMQTTClient(broker, port, clientID, userName, passWord)
	return &MqttClient{
		broker:   broker,
		port:     port,
		clientID: clientID,
		userName: userName,
		passWord: passWord,
		Company:  comp,
		client:   client,
	}
}

// Subscription 订阅方法 参数：主题,处理数据回调方法
func (m *MqttClient) Subscription(topic string, handleFunc func([]byte)) {
	messageHandler := func(client mqtt.Client, message mqtt.Message) {
		payload := message.Payload()
		if len(payload) > 0 {
			handleFunc(payload)
		}
	}
	sub := m.client.Subscribe(topic, 1, messageHandler)
	sub.Wait()

}

// Publish 发布方法 参数：主题 、消息
func (m *MqttClient) RawPublish(topic string, msg string) {
	token := m.client.Publish(topic, 0, false, msg)
	token.Wait()
}

// Publish 发布方法 参数：主题 、消息
func (m *MqttClient) Publish(topic string, msg interface{}) {
	token := m.client.Publish(topic, 0, false, msg)
	token.Wait()
}

// Close 关闭连接
func (m *MqttClient) Close() {
	m.client.Disconnect(250)
}
