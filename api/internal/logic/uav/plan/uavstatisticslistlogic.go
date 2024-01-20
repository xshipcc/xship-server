package plan

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavStatisticsListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavStatisticsListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavStatisticsListLogic {
	return &UavStatisticsListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavStatisticsListLogic) UavStatisticsList(req *types.ListUavStatisticsReq) (resp *types.ListUavStatisticsResp, err error) {
	// todo: add your logic here and delete this line

	return
}
