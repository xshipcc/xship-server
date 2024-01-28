package camera

import (
	"context"
	"encoding/json"
	"fmt"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type CamerasUpdateLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewCamerasUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *CamerasUpdateLogic {
	return &CamerasUpdateLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *CamerasUpdateLogic) CamerasUpdate(req *types.UpdateCamerasReq) (resp *types.UpdateCamerasResp, err error) {
	// 更新之前查询记录是否存在
	item, err := l.svcCtx.UavCameraModel.FindOne(l.ctx, req.Id)
	if err != nil {
		return nil, err
	}

	item.Name = req.Name
	item.Tunnel = req.Tunnel
	item.Status = req.Status
	item.Url = req.Url
	item.Platform = req.Platform
	item.Lat = req.Lat
	item.Lon = req.Lon
	item.Alt = req.Alt
	item.AiStatus = req.Ai_status
	err = l.svcCtx.UavCameraModel.Update(l.ctx, item)
	if err != nil {
		return nil, err
	}
	fmt.Printf("ai status   err:%d\n", req.Ai_status)

	var flydata uavlient.UavFlyData
	flydata.Cmd = "start_ai"
	flysend, _ := json.Marshal(flydata)
	l.svcCtx.MMQServer.Publish("fly_control", flysend)

	return &types.UpdateCamerasResp{
		Code:    "000000",
		Message: "保存成功",
	}, nil
}
