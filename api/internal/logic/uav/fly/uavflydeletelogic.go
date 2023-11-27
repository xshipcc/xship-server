package fly

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavFlyDeleteLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavFlyDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavFlyDeleteLogic {
	return &UavFlyDeleteLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavFlyDeleteLogic) UavFlyDelete(req *types.DeleteUavFlyReq) (resp *types.DeleteUavFlyResp, err error) {
	err = l.svcCtx.UavFlyModel.DeleteByIds(l.ctx, req.Ids)

	if err != nil {
		logx.WithContext(l.ctx).Errorf("查询无人机列表信息失败,异常:%s", err.Error())
		return nil, err
	}
	return &types.DeleteUavFlyResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
