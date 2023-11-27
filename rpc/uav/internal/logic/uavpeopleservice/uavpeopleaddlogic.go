package uavpeopleservicelogic

import (
	"context"
	"time"

	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPeopleAddLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavPeopleAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPeopleAddLogic {
	return &UavPeopleAddLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavPeopleAddLogic) UavPeopleAdd(in *uavlient.AddUavPeopleReq) (*uavlient.UavPeopleAddResp, error) {
	_, err := l.svcCtx.UavPeopleModel.Insert(l.ctx, &uavmodel.UavPeople{
		Username:   in.Username,
		Icon:       in.Icon,
		Level:      in.Level,
		Phone:      in.Phone,
		Status:     in.Status,
		Gender:     in.Gender,
		CreateTime: time.Now(),
	})

	return &uavlient.UavPeopleAddResp{}, err
}
