package flashpromotionservicelogic

import (
	"context"
	"time"
	"zero-admin/rpc/model/smsmodel"
	"zero-admin/rpc/sms/smsclient"

	"github.com/zeromicro/go-zero/core/logx"
	"zero-admin/rpc/sms/internal/svc"
)

type FlashPromotionAddLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewFlashPromotionAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *FlashPromotionAddLogic {
	return &FlashPromotionAddLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *FlashPromotionAddLogic) FlashPromotionAdd(in *smsclient.FlashPromotionAddReq) (*smsclient.FlashPromotionAddResp, error) {
	StartDate, _ := time.Parse("2006-01-02", in.StartDate)
	EndDate, _ := time.Parse("2006-01-02", in.EndDate)
	_, err := l.svcCtx.SmsFlashPromotionModel.Insert(l.ctx, &smsmodel.SmsFlashPromotion{
		Title:      in.Title,
		StartDate:  StartDate,
		EndDate:    EndDate,
		Status:     in.Status,
		CreateTime: time.Now(),
	})
	if err != nil {
		return nil, err
	}

	return &smsclient.FlashPromotionAddResp{}, nil
}
