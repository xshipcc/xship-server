package car

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type CarsListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewCarsListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *CarsListLogic {
	return &CarsListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *CarsListLogic) CarsList(req *types.ListCarsReq) (resp *types.ListCarsResp, err error) {
	count, _ := l.svcCtx.UavCarModel.Count(l.ctx)
	all, err := l.svcCtx.UavCarModel.FindAll(l.ctx, req.Current, req.PageSize)

	if err != nil {
		data, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("参数: %s,查询车车线异常:%s", string(data), err.Error())
		return nil, errorx.NewDefaultError("查询车车失败")
	}
	var list []*types.ListCarsData

	for _, dict := range *all {
		list = append(list, &types.ListCarsData{
			Id:     dict.Id,
			Name:   dict.Name,
			Card:   dict.Card,
			Status: dict.Status,
			Photo:  dict.Photo,
			Type:   dict.Type,
			Phone:  dict.Phone,
			Agency: dict.Agency,
		})
	}

	return &types.ListCarsResp{
		Code:     "000000",
		Message:  "查询字典成功",
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    count,
	}, nil
}
