package uavdeviceservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavDeviceListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavDeviceListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavDeviceListLogic {
	return &UavDeviceListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 获取设备列表
func (l *UavDeviceListLogic) UavDeviceList(in *uavlient.UavDeviceListReq) (*uavlient.UavDeviceListResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UavDeviceListResp{}, nil
}
