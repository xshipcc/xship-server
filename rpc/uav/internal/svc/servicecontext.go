package svc

import (
	"os/exec"
	"time"
	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/internal/config"

	"github.com/robfig/cron/v3"

	"github.com/zeromicro/go-zero/core/stores/redis"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
)

type ServiceContext struct {
	Config                config.Config
	UavDeviceModel        uavmodel.UavDeviceModel
	UavFlyHistoryModel    uavmodel.UavFlyHistoryModel
	FlyHistoryDetailModel uavmodel.UavFlyHistoryDetailModel
	UavFlyModel           uavmodel.UavFlyModel
	UavPeopleModel        uavmodel.UavPeopleModel
	UavNetworkModel       uavmodel.UavNetworkModel
	UavPlanModel          uavmodel.UavPlanModel
	UavMMQModel           uavmodel.UavMessageModel
	UavStatModel          uavmodel.UavStatisticsModel
	UavCameraModel        uavmodel.UavCameraModel
	CornServer            *cron.Cron
	StaticCornServer      *cron.Cron

	MMQServer MqttClient
	MyRedis   *redis.Redis
	Cmd       *exec.Cmd
	AICmd     *exec.Cmd
	CamAICmd  []*exec.Cmd
}

// Deadline implements context.Context.
func (*ServiceContext) Deadline() (deadline time.Time, ok bool) {
	panic("unimplemented")
}

// Done implements context.Context.
func (*ServiceContext) Done() <-chan struct{} {
	panic("unimplemented")
}

// Err implements context.Context.
func (*ServiceContext) Err() error {
	panic("unimplemented")
}

// Value implements context.Context.
func (*ServiceContext) Value(key any) any {
	panic("unimplemented")
}

func NewServiceContext(c config.Config) *ServiceContext {
	sqlConn := sqlx.NewMysql(c.Mysql.Datasource)
	newRedis := redis.New("127.0.0.1:6379")

	return &ServiceContext{
		Config:                c,
		UavDeviceModel:        uavmodel.NewUavDeviceModel(sqlConn),
		UavFlyHistoryModel:    uavmodel.NewUavFlyHistoryModel(sqlConn),
		FlyHistoryDetailModel: uavmodel.NewUavFlyHistoryDetailModel(sqlConn),
		UavFlyModel:           uavmodel.NewUavFlyModel(sqlConn),
		UavPeopleModel:        uavmodel.NewUavPeopleModel(sqlConn),
		UavNetworkModel:       uavmodel.NewUavNetworkModel(sqlConn),
		UavPlanModel:          uavmodel.NewUavPlanModel(sqlConn),
		UavMMQModel:           uavmodel.NewUavMessageModel(sqlConn),
		UavStatModel:          uavmodel.NewUavStatisticsModel(sqlConn),
		UavCameraModel:        uavmodel.NewUavCameraModel(sqlConn),

		MMQServer:  *NewMqttSubOption(c.MQTT.Broker, c.MQTT.Port, c.MQTT.ClientID, c.MQTT.UserName, c.MQTT.PassWord, c.MQTT.Company),
		CornServer: nil,

		StaticCornServer: nil,
		MyRedis:          newRedis,
		Cmd:              nil,
		AICmd:            nil,
	}
}
