package orderoperatehistorservicelogic

import (
	"context"
	"encoding/json"
	"zero-admin/rpc/oms/internal/svc"
	"zero-admin/rpc/oms/omsclient"

	"github.com/zeromicro/go-zero/core/logx"
)

type OrderOperateHistoryListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewOrderOperateHistoryListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *OrderOperateHistoryListLogic {
	return &OrderOperateHistoryListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *OrderOperateHistoryListLogic) OrderOperateHistoryList(in *omsclient.OrderOperateHistoryListReq) (*omsclient.OrderOperateHistoryListResp, error) {
	all, err := l.svcCtx.OmsOrderOperateHistoryModel.FindAll(l.ctx, in.Current, in.PageSize, 0)
	count, _ := l.svcCtx.OmsOrderOperateHistoryModel.Count(l.ctx)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询订单操作历史列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*omsclient.OrderOperateHistoryListData
	for _, item := range *all {

		list = append(list, &omsclient.OrderOperateHistoryListData{
			Id:          item.Id,
			OrderId:     item.OrderId,
			OperateMan:  item.OperateMan,
			CreateTime:  item.CreateTime.Format("2006-01-02 15:04:05"),
			OrderStatus: item.OrderStatus,
			Note:        item.Note.String,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询订单操作历史列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &omsclient.OrderOperateHistoryListResp{
		Total: count,
		List:  list,
	}, nil
}
