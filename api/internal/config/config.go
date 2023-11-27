package config

import (
	"github.com/zeromicro/go-zero/rest"
	"github.com/zeromicro/go-zero/zrpc"
)

type Config struct {
	rest.RestConf

	Uploads string
	//系统
	SysRpc zrpc.RpcClientConf
	//会员
	UmsRpc zrpc.RpcClientConf
	UavRpc zrpc.RpcClientConf
	//商品
	// PmsRpc zrpc.RpcClientConf
	// //订单
	// OmsRpc zrpc.RpcClientConf
	// //营销
	// SmsRpc zrpc.RpcClientConf
	Mysql struct {
		Datasource string
	}

	//内容
	CmsRpc zrpc.RpcClientConf

	Auth struct {
		AccessSecret string
		AccessExpire int64
	}

	Redis struct {
		Address string
		Pass    string
	}
}
