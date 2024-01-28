package camera

import (
	"context"
	"encoding/json"
	"fmt"
	"time"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type CamerasAddLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewCamerasAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *CamerasAddLogic {
	return &CamerasAddLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *CamerasAddLogic) CamerasAdd(req *types.AddCamerasReq) (resp *types.AddCamerasResp, err error) {
	_, err = l.svcCtx.UavCameraModel.Insert(l.ctx, &uavmodel.UavCamera{
		Name:       req.Name,
		Tunnel:     req.Tunnel,
		Status:     req.Status,
		Url:        req.Url,
		Platform:   req.Platform,
		Lat:        req.Lat,
		Lon:        req.Lon,
		Alt:        req.Alt,
		AiStatus:   req.Ai_status,
		CreateTime: time.Now(),
	})
	if err != nil {
		reqStr, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("添加摄像头,参数:%s,异常:%s", reqStr, err.Error())
		return nil, errorx.NewDefaultError("添加摄像头")
	}
	fmt.Printf("ai status   err:%d\n", req.Ai_status)

	var flydata uavlient.UavFlyData
	flydata.Cmd = "start_ai"
	flysend, _ := json.Marshal(flydata)
	l.svcCtx.MMQServer.Publish("fly_control", flysend)

	return &types.AddCamerasResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
