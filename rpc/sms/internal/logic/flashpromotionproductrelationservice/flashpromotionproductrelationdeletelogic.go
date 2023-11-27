package flashpromotionproductrelationservicelogic

import (
	"context"
	"zero-admin/rpc/sms/smsclient"

	"zero-admin/rpc/sms/internal/svc"

	"github.com/zeromicro/go-zero/core/logx"
)

type FlashPromotionProductRelationDeleteLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewFlashPromotionProductRelationDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) *FlashPromotionProductRelationDeleteLogic {
	return &FlashPromotionProductRelationDeleteLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *FlashPromotionProductRelationDeleteLogic) FlashPromotionProductRelationDelete(in *smsclient.FlashPromotionProductRelationDeleteReq) (*smsclient.FlashPromotionProductRelationDeleteResp, error) {
	err := l.svcCtx.SmsFlashPromotionProductRelationModel.DeleteByIds(l.ctx, in.Ids)

	if err != nil {
		return nil, err
	}

	return &smsclient.FlashPromotionProductRelationDeleteResp{}, nil
}
