package alert

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type AlertHistoryUpdateLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewAlertHistoryUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *AlertHistoryUpdateLogic {
	return &AlertHistoryUpdateLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *AlertHistoryUpdateLogic) AlertHistoryUpdate(req *types.UpdateAlertHistoryReq) (resp *types.UpdateAlertHistoryResp, err error) {
	// 更新之前查询记录是否存在
	item, err := l.svcCtx.UavMMQModel.FindOne(l.ctx, req.Id)
	if err != nil {
		return nil, err
	}

	item.Confirm = 1
	err = l.svcCtx.UavMMQModel.Update(l.ctx, item)
	if err != nil {
		return nil, err
	}

	return &types.UpdateAlertHistoryResp{
		Code:    "000000",
		Message: "保存成功",
	}, nil

}
