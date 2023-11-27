package ordersettingservicelogic

import (
	"context"
	"encoding/json"
	"zero-admin/rpc/oms/internal/svc"
	"zero-admin/rpc/oms/omsclient"

	"github.com/zeromicro/go-zero/core/logx"
)

type OrderSettingListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewOrderSettingListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *OrderSettingListLogic {
	return &OrderSettingListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *OrderSettingListLogic) OrderSettingList(in *omsclient.OrderSettingListReq) (*omsclient.OrderSettingListResp, error) {
	all, err := l.svcCtx.OmsOrderSettingModel.FindAll(l.ctx, in.Current, in.PageSize)
	count, _ := l.svcCtx.OmsOrderSettingModel.Count(l.ctx)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询订单设置列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*omsclient.OrderSettingListData
	for _, item := range *all {

		list = append(list, &omsclient.OrderSettingListData{
			Id:                  item.Id,
			FlashOrderOvertime:  item.FinishOvertime,
			NormalOrderOvertime: item.NormalOrderOvertime,
			ConfirmOvertime:     item.ConfirmOvertime,
			FinishOvertime:      item.FinishOvertime,
			CommentOvertime:     item.CommentOvertime,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询订单设置列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &omsclient.OrderSettingListResp{
		Total: count,
		List:  list,
	}, nil
}
