package device

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

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
	l.svcCtx.MMQServer.Publish("fly_control", "{'cmd':'start_uav'")

	return &types.DeleteUavDeviceResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
