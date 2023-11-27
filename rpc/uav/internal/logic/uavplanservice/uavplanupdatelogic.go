package uavplanservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPlanUpdateLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavPlanUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPlanUpdateLogic {
	return &UavPlanUpdateLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavPlanUpdateLogic) UavPlanUpdate(in *uavlient.UpdateUavPlanReq) (*uavlient.UpdateUavPlanResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UpdateUavPlanResp{}, nil
}
