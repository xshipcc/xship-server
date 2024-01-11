package uavmmqservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavMMQListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavMMQListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavMMQListLogic {
	return &UavMMQListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 获取消息列表
func (l *UavMMQListLogic) UavMMQList(in *uavlient.UavMMQListReq) (*uavlient.UavMMQListResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UavMMQListResp{}, nil
}
