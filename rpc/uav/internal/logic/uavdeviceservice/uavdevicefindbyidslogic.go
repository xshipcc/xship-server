package uavdeviceservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavDeviceFindByIdsLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavDeviceFindByIdsLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavDeviceFindByIdsLogic {
	return &UavDeviceFindByIdsLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 根据报警ids查询报警
func (l *UavDeviceFindByIdsLogic) UavDeviceFindByIds(in *uavlient.UavDeviceFindByIdsReq) (*uavlient.UavDeviceFindByIdsResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UavDeviceFindByIdsResp{}, nil
}
