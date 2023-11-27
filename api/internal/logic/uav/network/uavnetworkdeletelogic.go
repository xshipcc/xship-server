package network

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavNetworkDeleteLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavNetworkDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavNetworkDeleteLogic {
	return &UavNetworkDeleteLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavNetworkDeleteLogic) UavNetworkDelete(req *types.DeleteUavNetworkReq) (resp *types.DeleteUavNetworkResp, err error) {
	err = l.svcCtx.UavNetworkModel.DeleteByIds(l.ctx, req.Ids)

	if err != nil {
		logx.WithContext(l.ctx).Errorf("删除网络失败,异常:%s", err.Error())
		return nil, err
	}
	return &types.DeleteUavNetworkResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
