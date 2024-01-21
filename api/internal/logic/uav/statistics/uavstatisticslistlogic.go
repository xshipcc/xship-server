package statistics

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/common/errorx"
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
	count, _ := l.svcCtx.UavStatisticsModel.Count(l.ctx)
	all, err := l.svcCtx.UavStatisticsModel.FindAll(l.ctx, req.Current, req.PageSize)

	if err != nil {
		data, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("参数: %s,查询历史统计列表异常:%s", string(data), err.Error())
		return nil, errorx.NewDefaultError("查询历史统计失败")
	}
	var list []*types.ListtUavStatisticsData

	for _, dict := range *all {
		list = append(list, &types.ListtUavStatisticsData{
			Id:         dict.Id,
			Total:      dict.Id,
			Person:     dict.Person,
			Car:        dict.Car,
			Bicycle:    dict.Bicycle,
			Bus:        dict.Bus,
			Truck:      dict.Truck,
			BoxTruck:   dict.BoxTruck,
			Tricycle:   dict.Tricycle,
			Motorcycle: dict.Motorcycle,
			Smoke:      dict.Smoke,
			Fire:       dict.Fire,
			Remark:     dict.Remark,
			Snapshots:  dict.Snapshots,
			CreateTime: dict.CreateTime.Format("2006-01-02 15:04:05"),
		})
	}

	return &types.ListUavStatisticsResp{
		Code:     "000000",
		Message:  "查询字典成功",
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    count,
	}, nil
}
