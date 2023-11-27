package uavhistoryservicelogic

import (
	"context"
	"time"

	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavHistoryAddLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavHistoryAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavHistoryAddLogic {
	return &UavHistoryAddLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavHistoryAddLogic) UavHistoryAdd(in *uavlient.AddUavHistoryReq) (*uavlient.UavHistoryAddResp, error) {

	st, _ := time.Parse("2006-01-02 15:04:05", in.CreateTime)
	et, _ := time.Parse("2006-01-02 15:04:05", in.EndTime)
	_, err := l.svcCtx.UavFlyHistoryModel.Insert(l.ctx, &uavmodel.UavFlyHistory{
		UavId:      in.UavId,
		FlyId:      in.FlyID,
		Operator:   in.Operator,
		CreateTime: st,
		EndTime:    et,
	})

	return &uavlient.UavHistoryAddResp{}, err
}
