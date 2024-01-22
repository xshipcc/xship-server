package plan

import (
	"context"
	"encoding/json"
	"time"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPlanAddLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavPlanAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPlanAddLogic {
	return &UavPlanAddLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavPlanAddLogic) UavPlanAdd(req *types.AddUavPlanReq) (resp *types.AddUavPlanResp, err error) {
	_, err = l.svcCtx.UavPlanModel.Insert(l.ctx, &uavmodel.UavPlan{
		UavId:      req.Uav_id,
		UavName:    req.UAVName,
		Plan:       req.Plan,
		Name:       req.Name,
		FlyId:      req.Fly_id,
		RoadName:   req.FlyName,
		Status:     req.Status,
		CreateTime: time.Now(),
	})
	if err != nil {
		reqStr, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("添加网络失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, errorx.NewDefaultError("添加计划失败")
	}

	var flydata uavlient.UavFlyData
	flydata.Cmd = "corn"
	flysend, _ := json.Marshal(flydata)
	l.svcCtx.MMQServer.Publish("fly_control", flysend)

	return &types.AddUavPlanResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
