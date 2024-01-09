package device

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavDeviceDeleteLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavDeviceDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavDeviceDeleteLogic {
	return &UavDeviceDeleteLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavDeviceDeleteLogic) UavDeviceDelete(req *types.DeleteUavDeviceReq) (resp *types.DeleteUavDeviceResp, err error) {
	err = l.svcCtx.UavDeviceModel.DeleteByIds(l.ctx, req.Ids)

	if err != nil {
		logx.WithContext(l.ctx).Errorf("查询无人机列表信息失败,异常:%s", err.Error())
		return nil, err
	}
	var flydata uavlient.UavFlyData
	flydata.Cmd = "start_uav"

	flysend, _ := json.Marshal(flydata)

	l.svcCtx.MMQServer.Publish("fly_control", flysend)

	return &types.DeleteUavDeviceResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
