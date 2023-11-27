package history

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavHistoryAddLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavHistoryAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavHistoryAddLogic {
	return &UavHistoryAddLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavHistoryAddLogic) UavHistoryAdd(req *types.AddUavHistoryReq) (resp *types.AddUavHistoryResp, err error) {
	// todo: add your logic here and delete this line

	return
}
