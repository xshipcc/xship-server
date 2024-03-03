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

type UavPlanDeleteLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavPlanDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPlanDeleteLogic {
	return &UavPlanDeleteLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}
func contains(s []int64, e int64) bool {
	for _, a := range s {
		if a == e {
			return true
		}
	}
	return false
}

func (l *UavPlanDeleteLogic) UavPlanDelete(req *types.DeleteUavPlanReq) (resp *types.DeleteUavPlanResp, err error) {
	err = l.svcCtx.UavPlanModel.DeleteByIds(l.ctx, req.Ids)

	if err != nil {
		logx.WithContext(l.ctx).Errorf("删除网络失败,异常:%s", err.Error())
		return nil, err
	}

	plan, _ := l.svcCtx.Redis.Get("plan")
	plan_id, _ := strconv.ParseInt(plan, 10, 64)

	isContent := contains(req.Ids, plan_id)
	if isContent {
		return &types.DeleteUavPlanResp{
			Code:    "-1",
			Message: "无法删除正在执行的任务",
		}, nil
	}

	var flydata uavlient.UavFlyData
	flydata.Cmd = "corn"
	flysend, _ := json.Marshal(flydata)
	l.svcCtx.MMQServer.Publish("fly_control", flysend)

	return &types.DeleteUavPlanResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
