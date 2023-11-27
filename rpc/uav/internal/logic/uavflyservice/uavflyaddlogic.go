package uavflyservicelogic

import (
	"context"
	"time"

	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavFlyAddLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavFlyAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavFlyAddLogic {
	return &UavFlyAddLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 添加设备
func (l *UavFlyAddLogic) UavFlyAdd(in *uavlient.AddUavFlyReq) (*uavlient.UavFlyAddResp, error) {

	_, err := l.svcCtx.UavFlyModel.Insert(l.ctx, &uavmodel.UavFly{
		Name:       in.Name,
		Data:       in.Data,
		CreateTime: time.Now(),
		Creator:    in.Creator,
	})

	return &uavlient.UavFlyAddResp{}, err
}
