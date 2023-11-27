package flashpromotionlogservicelogic

import (
	"context"
	"encoding/json"
	"zero-admin/rpc/sms/internal/svc"
	"zero-admin/rpc/sms/smsclient"

	"github.com/zeromicro/go-zero/core/logx"
)

type FlashPromotionLogListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewFlashPromotionLogListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *FlashPromotionLogListLogic {
	return &FlashPromotionLogListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *FlashPromotionLogListLogic) FlashPromotionLogList(in *smsclient.FlashPromotionLogListReq) (*smsclient.FlashPromotionLogListResp, error) {
	all, err := l.svcCtx.SmsFlashPromotionLogModel.FindAll(l.ctx, in.Current, in.PageSize)
	count, _ := l.svcCtx.SmsFlashPromotionLogModel.Count(l.ctx)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询限时购通知记录列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*smsclient.FlashPromotionLogListData
	for _, item := range *all {

		list = append(list, &smsclient.FlashPromotionLogListData{
			Id:            item.Id,
			MemberId:      item.MemberId,
			ProductId:     item.ProductId,
			MemberPhone:   item.MemberPhone,
			ProductName:   item.ProductName,
			SubscribeTime: item.SubscribeTime.Format("2006-01-02 15:04:05"),
			SendTime:      item.SendTime.Format("2006-01-02 15:04:05"),
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询限时购通知记录列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &smsclient.FlashPromotionLogListResp{
		Total: count,
		List:  list,
	}, nil
}
