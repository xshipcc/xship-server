package uavpeopleservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPeopleUpdateLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavPeopleUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPeopleUpdateLogic {
	return &UavPeopleUpdateLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavPeopleUpdateLogic) UavPeopleUpdate(in *uavlient.UpdateUavPeopleReq) (*uavlient.UpdateUavPeopleResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.UpdateUavPeopleResp{}, nil
}
