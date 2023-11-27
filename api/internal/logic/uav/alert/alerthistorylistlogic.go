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

	count, _ := l.svcCtx.UavMMQModel.Count(l.ctx, req.HistoryID)
	all, err := l.svcCtx.UavMMQModel.FindAll(l.ctx, req.HistoryID, req.Current, req.PageSize)

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
			Starttime: dict.StartTime,
			Endtime:   dict.EndTime,
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
