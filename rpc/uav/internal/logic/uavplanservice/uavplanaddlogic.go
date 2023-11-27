package uavplanservicelogic

import (
	"context"
	"time"

	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPlanAddLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavPlanAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPlanAddLogic {
	return &UavPlanAddLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavPlanAddLogic) UavPlanAdd(in *uavlient.AddUavPlanReq) (*uavlient.UavPlanAddResp, error) {
	_, err := l.svcCtx.UavPlanModel.Insert(l.ctx, &uavmodel.UavPlan{
		UavId:      in.UavId,
		Plan:       in.Plan,
		FlyId:      in.FlyId,
		CreateTime: time.Now(),
	})
	return &uavlient.UavPlanAddResp{}, err
}
