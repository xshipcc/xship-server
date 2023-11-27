package car

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type CarsDeleteLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewCarsDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) *CarsDeleteLogic {
	return &CarsDeleteLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *CarsDeleteLogic) CarsDelete(req *types.DeleteCarsReq) (resp *types.DeleteCarsResp, err error) {
	err = l.svcCtx.UavCarModel.DeleteByIds(l.ctx, req.Ids)

	if err != nil {
		logx.WithContext(l.ctx).Errorf("查询car列表信息失败,异常:%s", err.Error())
		return nil, err
	}
	return &types.DeleteCarsResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
