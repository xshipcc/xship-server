package alert

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
	"zero-admin/rpc/uav/uavlient"

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

	today := time.Now().Format("2006-01-02")
	yesterday := time.Now().AddDate(0, 0, -1).Format("2006-01-02")
	week := time.Now().AddDate(0, 0, -7).Format("2006-01-02")

	var list []*types.ListAlertData

	points, _ := l.svcCtx.Redis.Lrange("points", 1, 50)

	var uavpoint uavlient.Uavpoints

	for _, pointvalue := range points {

		var pointBytes []byte
		pointBytes = []byte(pointvalue)

		json.Unmarshal(pointBytes, &uavpoint)
		list = append(list, &types.ListAlertData{
			Id:   0,
			Type: uavpoint.Type,
			Alt:  uavpoint.Alt,
			Lat:  uavpoint.Lat,
			Lon:  uavpoint.Lon,
		})

	}

	weekList := []int64{}

	all, err := l.svcCtx.UavStatisticsModel.FindBetween(l.ctx, week, today)
	for _, dict := range *all {
		weekList = append(weekList, dict.Total)
	}

	var uavStatistic uavlient.UavsStatistics

	history, err := l.svcCtx.Redis.Hget("history", today)
	historyC := []byte(history) // strB len: 8, cap: 8

	Today := make([]int64, 0)

	if err != nil {
		fmt.Printf("parse  err:%s\n", err)
	} else {
		json.Unmarshal(historyC, &uavStatistic)
		Today = append(Today, uavStatistic.Person)
		Today = append(Today, uavStatistic.Car)
		Today = append(Today, uavStatistic.Bicycle)
		Today = append(Today, uavStatistic.Bus)
		Today = append(Today, uavStatistic.Truck)
		Today = append(Today, uavStatistic.BoxTruck)
		Today = append(Today, uavStatistic.Tricycle)
		Today = append(Today, uavStatistic.Motorcycle)
		Today = append(Today, uavStatistic.Smoke)
		Today = append(Today, uavStatistic.Fire)
	}

	yestday := make([]int64, 0)
	history, err = l.svcCtx.Redis.Hget("history", yesterday)
	historyC = []byte(history) // strB len: 8, cap: 8

	if err != nil {
		fmt.Printf("parse  err:%s\n", err)
	} else {
		json.Unmarshal(historyC, &uavStatistic)
		yestday = append(yestday, uavStatistic.Person)
		yestday = append(yestday, uavStatistic.Car)
		yestday = append(yestday, uavStatistic.Bicycle)
		yestday = append(yestday, uavStatistic.Bus)
		yestday = append(yestday, uavStatistic.Truck)
		yestday = append(yestday, uavStatistic.BoxTruck)
		yestday = append(yestday, uavStatistic.Tricycle)
		yestday = append(yestday, uavStatistic.Motorcycle)
		yestday = append(yestday, uavStatistic.Smoke)
		yestday = append(yestday, uavStatistic.Fire)
	}

	datyeast := &types.Datayesterday{
		TodayData: Today,
		YestData:  yestday,
	}

	AlertConfirmsList := []int64{1, 2, 4, 5, 5, 6, 3, 3, 2, 1}
	AlertNotConfirmsList := []int64{1, 2, 4, 5, 5, 6, 3, 3, 2, 1}
	AlertTotalsList := []int64{1, 2, 4, 5, 5, 6, 3, 3, 2, 1}

	intall, err2 := l.svcCtx.UavMMQModel.AleretCount(l.ctx, today, -1)
	if err2 != nil {
		fmt.Printf("count get   err:%s\n", err)
	} else {

		for _, dict := range *intall {
			fmt.Printf("%d : %d", dict.Type, dict.Count)
			AlertTotalsList[dict.Type] = dict.Count
		}
	}

	intnot, err2 := l.svcCtx.UavMMQModel.AleretCount(l.ctx, today, 0)
	if err2 != nil {
		fmt.Printf("count get   err:%s\n", err)
	} else {

		for _, dict := range *intnot {
			fmt.Printf("%d : %d", dict.Type, dict.Count)
			AlertNotConfirmsList[dict.Type] = dict.Count
		}
	}

	intok, err2 := l.svcCtx.UavMMQModel.AleretCount(l.ctx, today, 1)
	if err2 != nil {
		fmt.Printf("count get   err:%s\n", err)
	} else {

		for _, dict := range *intok {
			fmt.Printf("%d : %d", dict.Type, dict.Count)
			AlertConfirmsList[dict.Type] = dict.Count
		}
	}

	countall, _ := l.svcCtx.UavFlyHistoryModel.CountStatus(l.ctx, -1)

	countcomplete, _ := l.svcCtx.UavFlyHistoryModel.CountStatus(l.ctx, 1)

	countfly, _ := l.svcCtx.UavFlyModel.Count(l.ctx, -1)

	return &types.ListAlertStatisticsResp{
		Data:             list,
		WeekCount:        weekList,
		TodayYesterday:   datyeast,
		AlertTotals:      AlertTotalsList,
		AlertConfirms:    AlertConfirmsList,
		AlertNotConfirms: AlertNotConfirmsList,
		Total:            countall,
		Completion:       countcomplete,
		TotalTime:        3,
		FlyTotal:         countfly,
	}, nil
}
