package alert

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type AlertItemConfirmLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewAlertItemConfirmLogic(ctx context.Context, svcCtx *svc.ServiceContext) *AlertItemConfirmLogic {
	return &AlertItemConfirmLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *AlertItemConfirmLogic) AlertItemConfirm(req *types.ConfirmAlertHistoryReq) (resp *types.ConfirmAlertHistoryResp, err error) {
	// todo: add your logic here and delete this line

	return
}
