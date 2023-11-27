package uavdeviceservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavDeviceFindByIdLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavDeviceFindByIdLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavDeviceFindByIdLogic {
	return &UavDeviceFindByIdLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 根据报警id查询报警
func (l *UavDeviceFindByIdLogic) UavDeviceFindById(in *uavlient.UavDeviceFindByIdReq) (*uavlient.UavDeviceFindByIdResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UavDeviceFindByIdResp{}, nil
}
