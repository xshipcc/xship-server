package camera

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

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
	return &types.DeleteCamerasResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
