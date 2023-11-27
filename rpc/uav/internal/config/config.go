package config

import "github.com/zeromicro/go-zero/zrpc"

type Config struct {
	zrpc.RpcServerConf

	Mysql struct {
		Datasource string
	}
	MQTT struct {
		Broker   string
		ClientID string
		UserName string
		PassWord string
		Port     int
		Company  string //公司名称
	}
	AIRPORT struct {
		IP    string
		PORT  int
		RPORT int
	}
	TopicAlert string
	TopicUav   string
}
