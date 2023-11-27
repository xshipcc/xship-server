package uavdeviceservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavDeviceUpdateLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavDeviceUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavDeviceUpdateLogic {
	return &UavDeviceUpdateLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 修改设备表
func (l *UavDeviceUpdateLogic) UavDeviceUpdate(in *uavlient.UavDeviceAddReq) (*uavlient.UavDeviceAddResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UavDeviceAddResp{}, nil
}
