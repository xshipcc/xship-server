package uavflyservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavFlyFindByIdLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavFlyFindByIdLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavFlyFindByIdLogic {
	return &UavFlyFindByIdLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 根据设备d查询报警
func (l *UavFlyFindByIdLogic) UavFlyFindById(in *uavlient.UavFlyFindByIdReq) (*uavlient.ListUavFlyResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.ListUavFlyResp{}, nil
}
