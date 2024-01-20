package svc

import (
	"zero-admin/api/internal/config"
	"zero-admin/api/internal/middleware"
	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/sys/client/configservice"
	"zero-admin/rpc/sys/client/deptservice"
	"zero-admin/rpc/sys/client/dictservice"
	"zero-admin/rpc/sys/client/jobservice"
	"zero-admin/rpc/sys/client/loginlogservice"
	"zero-admin/rpc/sys/client/menuservice"
	"zero-admin/rpc/sys/client/roleservice"
	"zero-admin/rpc/sys/client/syslogservice"
	"zero-admin/rpc/sys/client/userservice"

	"github.com/zeromicro/go-zero/core/stores/redis"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
	"github.com/zeromicro/go-zero/rest"
	"github.com/zeromicro/go-zero/zrpc"
)

type ServiceContext struct {
	Config   config.Config
	CheckUrl rest.Middleware
	AddLog   rest.Middleware

	//系统相关

	ConfigService   configservice.ConfigService
	DeptService     deptservice.DeptService
	DictService     dictservice.DictService
	JobService      jobservice.JobService
	LoginLogService loginlogservice.LoginLogService
	SysLogService   syslogservice.SysLogService
	MenuService     menuservice.MenuService
	RoleService     roleservice.RoleService
	UserService     userservice.UserService

	UavDeviceModel     uavmodel.UavDeviceModel
	UavFlyHistoryModel uavmodel.UavFlyHistoryModel
	UavFlyModel        uavmodel.UavFlyModel
	UavPeopleModel     uavmodel.UavPeopleModel
	UavNetworkModel    uavmodel.UavNetworkModel
	UavPlanModel       uavmodel.UavPlanModel
	UavMMQModel        uavmodel.UavMessageModel
	UavCameraModel     uavmodel.UavCameraModel
	UavCarModel        uavmodel.UavCarModel
	MMQServer          MqttClient

	Redis *redis.Redis
}

func NewServiceContext(c config.Config) *ServiceContext {
	newRedis := redis.New(c.Redis.Address, redisConfig(c))
	// umsClient := zrpc.MustNewClient(c.UmsRpc)
	sysClient := zrpc.MustNewClient(c.SysRpc)
	// uavClient := zrpc.MustNewClient(c.UavRpc)
	sqlConn := sqlx.NewMysql(c.Mysql.Datasource)

	logService := syslogservice.NewSysLogService(sysClient)
	return &ServiceContext{
		Config: c,

		ConfigService:   configservice.NewConfigService(sysClient),
		DeptService:     deptservice.NewDeptService(sysClient),
		DictService:     dictservice.NewDictService(sysClient),
		JobService:      jobservice.NewJobService(sysClient),
		LoginLogService: loginlogservice.NewLoginLogService(sysClient),
		SysLogService:   logService,
		MenuService:     menuservice.NewMenuService(sysClient),
		RoleService:     roleservice.NewRoleService(sysClient),
		UserService:     userservice.NewUserService(sysClient),

		//无人机

		UavDeviceModel:     uavmodel.NewUavDeviceModel(sqlConn),
		UavFlyHistoryModel: uavmodel.NewUavFlyHistoryModel(sqlConn),
		UavFlyModel:        uavmodel.NewUavFlyModel(sqlConn),
		UavPeopleModel:     uavmodel.NewUavPeopleModel(sqlConn),
		UavNetworkModel:    uavmodel.NewUavNetworkModel(sqlConn),
		UavPlanModel:       uavmodel.NewUavPlanModel(sqlConn),
		UavMMQModel:        uavmodel.NewUavMessageModel(sqlConn),
		UavCameraModel:     uavmodel.NewUavCameraModel(sqlConn),
		UavCarModel:        uavmodel.NewUavCarModel(sqlConn),

		CheckUrl:  middleware.NewCheckUrlMiddleware(newRedis).Handle,
		AddLog:    middleware.NewAddLogMiddleware(logService).Handle,
		MMQServer: *NewMqttSubOption(c.MQTT.Broker, c.MQTT.Port, c.MQTT.ClientID, c.MQTT.UserName, c.MQTT.PassWord, c.MQTT.Company),

		Redis: newRedis,
	}
}

func redisConfig(c config.Config) redis.Option {
	return func(r *redis.Redis) {
		r.Type = redis.NodeType
		r.Pass = c.Redis.Pass
	}
}
