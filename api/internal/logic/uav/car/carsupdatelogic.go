package car

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type CarsUpdateLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewCarsUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *CarsUpdateLogic {
	return &CarsUpdateLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *CarsUpdateLogic) CarsUpdate(req *types.UpdateCarsReq) (resp *types.UpdateCarsResp, err error) {
	// 更新之前查询记录是否存在
	item, err := l.svcCtx.UavCarModel.FindOne(l.ctx, req.Id)
	if err != nil {
		return nil, err
	}

	item.Id = req.Id
	item.Name = req.Name
	item.Card = req.Card
	item.Status = req.Status
	item.Photo = req.Photo
	item.Type = req.Type
	item.Phone = req.Phone
	item.Agency = req.Agency
	err = l.svcCtx.UavCarModel.Update(l.ctx, item)
	if err != nil {
		return nil, err
	}

	return &types.UpdateCarsResp{
		Code:    "000000",
		Message: "保存成功",
	}, nil
}
