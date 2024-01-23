package plan

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPlanListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavPlanListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPlanListLogic {
	return &UavPlanListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavPlanListLogic) UavPlanList(req *types.ListUavPlanReq) (resp *types.ListUavPlanResp, err error) {
	count, _ := l.svcCtx.UavPlanModel.Count(l.ctx, req.Uav_id, req.Fly_id)
	all, err := l.svcCtx.UavPlanModel.FindAll(l.ctx, req.Uav_id, req.Fly_id, req.Current, req.PageSize)

	if err != nil {
		data, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("参数: %s,查询计划列表异常:%s", string(data), err.Error())
		return nil, errorx.NewDefaultError("查询计划失败")
	}
	var list []*types.ListtUavPlanData

	for _, dict := range *all {
		list = append(list, &types.ListtUavPlanData{
			Id:      dict.Id,
			Name:    dict.Name,
			UAVName: dict.UavName,
			Uav_id:  dict.UavId,
			FlyName: dict.RoadName,
			Plan:    dict.Plan,
			Fly_id:  dict.FlyId,
			Status:  dict.Status,
		})
	}

	return &types.ListUavPlanResp{
		Code:     "000000",
		Message:  "查询字典成功",
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    count,
	}, nil
}
