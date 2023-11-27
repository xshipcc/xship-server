package uavnetworkservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavNetworkUpdateLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavNetworkUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavNetworkUpdateLogic {
	return &UavNetworkUpdateLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavNetworkUpdateLogic) UavNetworkUpdate(in *uavlient.UpdateUavNetworkReq) (*uavlient.UpdateUavNetworkResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UpdateUavNetworkResp{}, nil
}
