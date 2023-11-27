package uavhistoryservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavHistoryFindByIdLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavHistoryFindByIdLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavHistoryFindByIdLogic {
	return &UavHistoryFindByIdLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavHistoryFindByIdLogic) UavHistoryFindById(in *uavlient.UavHistoryFindByIdReq) (*uavlient.ListUavHistoryResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.ListUavHistoryResp{}, nil
}
