package alert

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type StatisticsLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewStatisticsLogic(ctx context.Context, svcCtx *svc.ServiceContext) *StatisticsLogic {
	return &StatisticsLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *StatisticsLogic) Statistics(req *types.UpdateAlertHistoryReq) (resp *types.ListAlertStatisticsResp, err error) {

	if err != nil {
		return nil, err
	}

	return &types.ListAlertStatisticsResp{
		Total:      0,
		Completion: 2,
		TotalTime:  3,
	}, nil
}
