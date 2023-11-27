package uavpeopleservicelogic

import (
	"context"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPeopleFindByIdLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavPeopleFindByIdLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPeopleFindByIdLogic {
	return &UavPeopleFindByIdLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavPeopleFindByIdLogic) UavPeopleFindById(in *uavlient.UavPeopleFindByIdReq) (*uavlient.ListUavPeopleResp, error) {
	// todo: add your logic here and delete this line

	return &uavlient.ListUavPeopleResp{}, nil
}
