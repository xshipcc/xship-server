package uavflyservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavFlyUpdateLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavFlyUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavFlyUpdateLogic {
	return &UavFlyUpdateLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 修改设备表
func (l *UavFlyUpdateLogic) UavFlyUpdate(in *uavlient.UpdateUavFlyReq) (*uavlient.UpdateUavFlyResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UpdateUavFlyResp{}, nil
}
