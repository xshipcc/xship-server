package plan

import (
	"context"
	"encoding/json"

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

func (l *UavPlanDeleteLogic) UavPlanDelete(req *types.DeleteUavPlanReq) (resp *types.DeleteUavPlanResp, err error) {
	err = l.svcCtx.UavPlanModel.DeleteByIds(l.ctx, req.Ids)

	if err != nil {
		logx.WithContext(l.ctx).Errorf("删除网络失败,异常:%s", err.Error())
		return nil, err
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
