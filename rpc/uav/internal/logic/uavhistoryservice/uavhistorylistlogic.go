package uavhistoryservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavHistoryListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavHistoryListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavHistoryListLogic {
	return &UavHistoryListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavHistoryListLogic) UavHistoryList(in *uavlient.ListUavHistoryReq) (*uavlient.ListUavHistoryResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.ListUavHistoryResp{}, nil
}
