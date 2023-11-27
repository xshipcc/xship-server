package logic

import (
	"context"
	"zero-admin/api/internal/common/errorx"
	"zero-admin/rpc/oms/omsclient"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type OrderSettingDeleteLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewOrderSettingDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) OrderSettingDeleteLogic {
	return OrderSettingDeleteLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *OrderSettingDeleteLogic) OrderSettingDelete(req types.DeleteOrderSettingReq) (*types.DeleteOrderSettingResp, error) {
	_, err := l.svcCtx.OrderSettingService.OrderSettingDelete(l.ctx, &omsclient.OrderSettingDeleteReq{
		Ids: req.Ids,
	})

	if err != nil {
		logx.WithContext(l.ctx).Errorf("根据Id: %d,删除订单设置异常:%s", req.Ids, err.Error())
		return nil, errorx.NewDefaultError("删除订单设置失败")
	}

	return &types.DeleteOrderSettingResp{
		Code:    "000000",
		Message: "",
	}, nil
}
