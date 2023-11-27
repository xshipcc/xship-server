package plan

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

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
	return &types.DeleteUavPlanResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
