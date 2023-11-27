package uavnetworkservicelogic

import (
	"context"
	"time"

	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavNetworkAddLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavNetworkAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavNetworkAddLogic {
	return &UavNetworkAddLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavNetworkAddLogic) UavNetworkAdd(in *uavlient.AddUavNetworkReq) (*uavlient.UavNetworkAddResp, error) {

	_, err := l.svcCtx.UavNetworkModel.Insert(l.ctx, &uavmodel.UavNetwork{

		Name:       in.Name,
		Band:       in.Band,
		Type:       in.Type,
		CreateTime: time.Now(),
	})

	return &uavlient.UavNetworkAddResp{}, err
}
