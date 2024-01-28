package camera

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type CamerasDeleteLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewCamerasDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) *CamerasDeleteLogic {
	return &CamerasDeleteLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *CamerasDeleteLogic) CamerasDelete(req *types.DeleteCamerasReq) (resp *types.DeleteCamerasResp, err error) {
	err = l.svcCtx.UavCameraModel.DeleteByIds(l.ctx, req.Ids)

	if err != nil {
		logx.WithContext(l.ctx).Errorf("查询摄像头列表信息失败,异常:%s", err.Error())
		return nil, err
	}
	var flydata uavlient.UavFlyData
	flydata.Cmd = "start_ai"
	flysend, _ := json.Marshal(flydata)
	l.svcCtx.MMQServer.Publish("fly_control", flysend)
	return &types.DeleteCamerasResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
