package network

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavNetworkUpdateLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavNetworkUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavNetworkUpdateLogic {
	return &UavNetworkUpdateLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavNetworkUpdateLogic) UavNetworkUpdate(req *types.UpdateUavNetworkReq) (resp *types.UpdateUavNetworkResp, err error) {
	item, err := l.svcCtx.UavNetworkModel.FindOne(l.ctx, req.Id)
	if err != nil {
		return nil, err
	}

	item.Name = req.Name
	item.Type = req.Type
	item.Band = req.Band
	err = l.svcCtx.UavNetworkModel.Update(l.ctx, item)
	if err != nil {
		return nil, err
	}

	return &types.UpdateUavNetworkResp{
		Code:    "000000",
		Message: "保存成功",
	}, nil
}
