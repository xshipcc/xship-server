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

	var list []*types.ListAlertData

	list = append(list, &types.ListAlertData{
		Id:   1,
		Type: 1,
		Alt:  0,
		Lat:  0,
		Lon:  0,
	})

	list = append(list, &types.ListAlertData{
		Id:   1,
		Type: 1,
		Alt:  3,
		Lat:  3,
		Lon:  3,
	})

	list = append(list, &types.ListAlertData{
		Id:   1,
		Type: 1,
		Alt:  4,
		Lat:  5,
		Lon:  6,
	})

	list = append(list, &types.ListAlertData{
		Id:   1,
		Type: 1,
		Alt:  2,
		Lat:  3,
		Lon:  7,
	})

	weekList := []int64{1, 2, 5, 20, 10, 7}

	Today := make([]int64, 0)
	Today = append(Today, 1)
	Today = append(Today, 1)
	Today = append(Today, 1)

	yestday := make([]int64, 0)
	yestday = append(yestday, 1)
	yestday = append(yestday, 1)
	yestday = append(yestday, 1)

	datyeast := &types.Datayesterday{
		TodayData: Today,
		YestData:  yestday,
	}

	AlertConfirmsList := []int64{1, 2, 4, 5, 5, 6, 3, 3, 2}

	AlertNotConfirmsList := []int64{1, 2, 2, 5, 6, 7, 4, 3, 2, 1}

	AlertTotalsList := []int64{4, 5, 2, 2, 10, 7, 4, 8, 8, 8}

	return &types.ListAlertStatisticsResp{
		Data:             list,
		WeekCount:        weekList,
		TodayYesterday:   datyeast,
		AlertTotals:      AlertTotalsList,
		AlertConfirms:    AlertConfirmsList,
		AlertNotConfirms: AlertNotConfirmsList,
		Total:            32,
		Completion:       2,
		TotalTime:        3,
	}, nil
}
