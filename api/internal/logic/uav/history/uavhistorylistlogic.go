package history

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavHistoryListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavHistoryListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavHistoryListLogic {
	return &UavHistoryListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavHistoryListLogic) UavHistoryList(req *types.ListUavHistoryReq) (resp *types.ListUavHistoryResp, err error) {
	count, _ := l.svcCtx.UavFlyHistoryModel.Count(l.ctx, req.HistoryID, req.Status, req.CreateTime)
	all, err := l.svcCtx.UavFlyHistoryModel.FindAll(l.ctx, req.HistoryID, req.Status, req.CreateTime, req.Current, req.PageSize)

	if err != nil {
		data, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("参数: %s,查询历史列表异常:%s", string(data), err.Error())
		return nil, errorx.NewDefaultError("查询字典失败")
	}
	var list []*types.ListtUavHistoryData

	for _, dict := range *all {
		list = append(list, &types.ListtUavHistoryData{
			Id:         dict.Id,
			UavId:      dict.UavId,
			UavName:    dict.UavName,
			FlyID:      dict.FlyId,
			FlyName:    dict.RoadName,
			Operator:   dict.Operator,
			Status:     dict.Status,
			Remark:     dict.Remark,
			CreateTime: dict.CreateTime.Format("2006-01-02 15:04:05"),
			EndTime:    dict.EndTime.Format("2006-01-02 15:04:05"),
		})
	}

	return &types.ListUavHistoryResp{
		Code:     "000000",
		Message:  "查询字典成功",
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    count,
	}, nil

}
