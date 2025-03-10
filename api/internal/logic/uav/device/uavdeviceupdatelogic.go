package device

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavDeviceUpdateLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavDeviceUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavDeviceUpdateLogic {
	return &UavDeviceUpdateLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavDeviceUpdateLogic) UavDeviceUpdate(req *types.UpdateUavDeviceReq) (resp *types.UpdateUavDeviceResp, err error) {
	// 更新之前查询记录是否存在
	item, err := l.svcCtx.UavDeviceModel.FindOne(l.ctx, req.Id)
	if err != nil {
		return nil, err
	}

	item.Name = req.Name
	item.Ip = req.Ip
	item.Port = req.Port
	item.RPort = req.R_Port
	item.HangarIp = req.Hangar_ip
	item.HangarPort = req.Hangar_port
	item.HangarRport = req.Hangar_rport
	item.CamIp = req.Cam_ip
	item.CamPort = req.Cam_port
	item.CamUrl = req.Cam_url
	item.Network = req.Network
	item.Joystick = req.Joystick
	item.UavZubo = req.UavZubo
	item.Status = req.Status

	err = l.svcCtx.UavDeviceModel.Update(l.ctx, item)
	if err != nil {
		return nil, err
	}

	var flydata uavlient.UavFlyData
	flydata.Cmd = "start_uav"

	flysend, _ := json.Marshal(flydata)

	l.svcCtx.MMQServer.Publish("fly_control", flysend)
	return &types.UpdateUavDeviceResp{
		Code:    "000000",
		Message: "保存成功",
	}, nil
}
