package uavnetworkservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavNetworkFindByIdLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavNetworkFindByIdLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavNetworkFindByIdLogic {
	return &UavNetworkFindByIdLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavNetworkFindByIdLogic) UavNetworkFindById(in *uavlient.UavNetworkFindByIdReq) (*uavlient.ListUavNetworkResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.ListUavNetworkResp{}, nil
}
