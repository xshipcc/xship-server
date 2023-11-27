package uavmmqservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavMMQFindByIdsLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavMMQFindByIdsLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavMMQFindByIdsLogic {
	return &UavMMQFindByIdsLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 根据设备ids查询报警
func (l *UavMMQFindByIdsLogic) UavMMQFindByIds(in *uavlient.UavMMQFindByIdsReq) (*uavlient.UavMMQFindByIdsResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UavMMQFindByIdsResp{}, nil
}
