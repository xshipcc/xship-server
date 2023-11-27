package uavmmqservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavMMQConfirmByIdLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavMMQConfirmByIdLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavMMQConfirmByIdLogic {
	return &UavMMQConfirmByIdLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 根据设备d查询报警
func (l *UavMMQConfirmByIdLogic) UavMMQConfirmById(in *uavlient.UavMMQFindByIdReq) (*uavlient.UavMMQFindByIdResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UavMMQFindByIdResp{}, nil
}
