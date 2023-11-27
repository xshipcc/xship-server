package uavplanservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPlanFindByIdLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavPlanFindByIdLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPlanFindByIdLogic {
	return &UavPlanFindByIdLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavPlanFindByIdLogic) UavPlanFindById(in *uavlient.UavPlanFindByIdReq) (*uavlient.ListUavPlanResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.ListUavPlanResp{}, nil
}
