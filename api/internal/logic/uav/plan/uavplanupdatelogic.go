package plan

import (
	"context"
	"encoding/json"
	"strconv"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPlanUpdateLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavPlanUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPlanUpdateLogic {
	return &UavPlanUpdateLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavPlanUpdateLogic) UavPlanUpdate(req *types.UpdateUavPlanReq) (resp *types.UpdateUavPlanResp, err error) {
	item, err := l.svcCtx.UavPlanModel.FindOne(l.ctx, req.Id)
	if err != nil {
		return nil, err
	}
	item.UavId = req.Uav_id
	item.Plan = req.Plan
	item.FlyId = req.Fly_id
	item.UavName = req.UAVName
	item.Name = req.Name
	item.Status = req.Status
	item.RoadName = req.FlyName

	plan, _ := l.svcCtx.Redis.Get("plan")
	plan_id, _ := strconv.ParseInt(plan, 10, 64)

	logx.WithContext(l.ctx).Infof("------------------无人机更新,参数：%d  %d", plan_id ,req.Id )

	if plan_id == req.Id {
		return &types.UpdateUavPlanResp{
			Code:    "-1",
			Message: "无法更新正在执行的任务",
		}, nil
	}

	err = l.svcCtx.UavPlanModel.Update(l.ctx, item)
	if err != nil {
		return nil, err
	}

	var flydata uavlient.UavFlyData
	flydata.Cmd = "corn"
	flysend, _ := json.Marshal(flydata)
	l.svcCtx.MMQServer.Publish("fly_control", flysend)

	return &types.UpdateUavPlanResp{
		Code:    "000000",
		Message: "保存成功",
	}, nil
}
