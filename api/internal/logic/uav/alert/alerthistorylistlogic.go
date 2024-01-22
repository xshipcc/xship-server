package alert

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type AlertHistoryListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewAlertHistoryListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *AlertHistoryListLogic {
	return &AlertHistoryListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *AlertHistoryListLogic) AlertHistoryList(req *types.ListAlertHistoryReq) (resp *types.ListAlertHistoryResp, err error) {
	// Type        int64  `json:"type"`//'消息类型:0-全部 1-巡检路线 2-入侵 3-烟火 4-人员 5-车辆',
	// 	Platform    int64  `json:"platform"` //监控的平台 '使用平台：0-全部 1-飞机 2-摄像头;3-机库;4-AI',
	// 	HistoryID 	int64  `json:"history_id"`// 巡检路线id 告警信息和巡检路线id绑定 巡检路线->告警路线 一对多
	// 	Confirm       int64  `json:"confirm"`//是否是 审查过的。
	//		Count(ctx context.Context, history_type int64, platform int64, history_id int64, confirm int64) (int64, error)

	count, _ := l.svcCtx.UavMMQModel.Count(l.ctx, req.Type, req.Starttime, req.Platform, req.HistoryID, req.Confirm)
	all, err := l.svcCtx.UavMMQModel.FindAll(l.ctx, req.Type, req.Starttime, req.Platform, req.HistoryID, req.Confirm, req.Current, req.PageSize)

	// respList, err := l.svcCtx.UavMMQModel.(l.ctx, &uavlient.UavMMQListReq{
	// 	Current:  req.Current,
	// 	PageSize: req.PageSize,
	// })
	if err != nil {
		data, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("参数: %s,查询报警列表异常:%s", string(data), err.Error())
		return nil, errorx.NewDefaultError("查询报警失败")
	}
	var list []*types.ListAlertHistoryData

	for _, dict := range *all {
		list = append(list, &types.ListAlertHistoryData{
			Id:        dict.Id,
			Name:      dict.Name,
			Image:     dict.Image,
			Type:      dict.Type,
			Code:      dict.Code,
			Level:     dict.Level,
			Count:     dict.Count,
			Platform:  dict.Platform,
			Starttime: dict.CreateTime.Format("2006-01-02 15:04:05"),
			Note:      dict.Note,
			Lat:       dict.Lat,
			Lon:       dict.Lon,
			Alt:       dict.Alt,
			HistoryID: dict.HistoryId,
			Confirm:   dict.Confirm,
		})
	}

	return &types.ListAlertHistoryResp{
		Code:     "000000",
		Message:  "查询字典成功",
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    count,
	}, nil
}
