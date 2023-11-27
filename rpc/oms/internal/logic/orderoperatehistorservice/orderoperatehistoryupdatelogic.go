package orderoperatehistorservicelogic

import (
	"context"
	"database/sql"
	"time"
	"zero-admin/rpc/model/omsmodel"
	"zero-admin/rpc/oms/omsclient"

	"zero-admin/rpc/oms/internal/svc"

	"github.com/zeromicro/go-zero/core/logx"
)

type OrderOperateHistoryUpdateLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewOrderOperateHistoryUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *OrderOperateHistoryUpdateLogic {
	return &OrderOperateHistoryUpdateLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *OrderOperateHistoryUpdateLogic) OrderOperateHistoryUpdate(in *omsclient.OrderOperateHistoryUpdateReq) (*omsclient.OrderOperateHistoryUpdateResp, error) {
	CreateTime, _ := time.Parse("2006-01-02 15:04:05", in.CreateTime)
	err := l.svcCtx.OmsOrderOperateHistoryModel.Update(l.ctx, &omsmodel.OmsOrderOperateHistory{
		OrderId:     in.OrderId,
		OperateMan:  in.OperateMan,
		CreateTime:  CreateTime,
		OrderStatus: in.OrderStatus,
		Note:        sql.NullString{String: in.Note, Valid: true},
	})
	if err != nil {
		return nil, err
	}

	return &omsclient.OrderOperateHistoryUpdateResp{}, nil
}
