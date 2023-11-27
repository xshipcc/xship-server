package uavdeviceservicelogic

import (
	"context"

	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavDeviceAddLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavDeviceAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavDeviceAddLogic {
	return &UavDeviceAddLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 添加报警
func (l *UavDeviceAddLogic) UavDeviceAdd(in *uavlient.UavDeviceAddReq) (*uavlient.UavDeviceAddResp, error) {
	_, err := l.svcCtx.UavDeviceModel.Insert(l.ctx, &uavmodel.UavDevice{
		Name:       in.Name,
		Ip:         in.Ip,
		Port:       in.Port,
		HangarIp:   in.HangarIp,
		HangarPort: in.HangarPort,
	})

	return &uavlient.UavDeviceAddResp{}, err
}
