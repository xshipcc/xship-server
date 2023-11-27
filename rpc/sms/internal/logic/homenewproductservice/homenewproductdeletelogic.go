package homenewproductservicelogic

import (
	"context"
	"zero-admin/rpc/sms/smsclient"

	"github.com/zeromicro/go-zero/core/logx"
	"zero-admin/rpc/sms/internal/svc"
)

type HomeNewProductDeleteLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewHomeNewProductDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) *HomeNewProductDeleteLogic {
	return &HomeNewProductDeleteLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *HomeNewProductDeleteLogic) HomeNewProductDelete(in *smsclient.HomeNewProductDeleteReq) (*smsclient.HomeNewProductDeleteResp, error) {
	err := l.svcCtx.SmsHomeNewProductModel.DeleteByIds(l.ctx, in.Ids)

	if err != nil {
		return nil, err
	}

	return &smsclient.HomeNewProductDeleteResp{}, nil
}
