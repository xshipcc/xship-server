package uavhistoryservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavHistoryUpdateLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavHistoryUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavHistoryUpdateLogic {
	return &UavHistoryUpdateLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavHistoryUpdateLogic) UavHistoryUpdate(in *uavlient.UpdateUavHistoryReq) (*uavlient.UpdateUavHistoryResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UpdateUavHistoryResp{}, nil
}
