package car

import (
	"context"
	"encoding/json"
	"time"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
	"zero-admin/rpc/model/uavmodel"

	"github.com/zeromicro/go-zero/core/logx"
)

type CarsAddLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewCarsAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *CarsAddLogic {
	return &CarsAddLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *CarsAddLogic) CarsAdd(req *types.AddCarsReq) (resp *types.AddCarsResp, err error) {
	_, err = l.svcCtx.UavCarModel.Insert(l.ctx, &uavmodel.UavCar{
		Name:       req.Name,
		Card:       req.Card,
		Status:     req.Status,
		Photo:      req.Photo,
		Type:       req.Type,
		Phone:      req.Phone,
		Agency:     req.Agency,
		CreateTime: time.Now(),
	})

	if err != nil {
		reqStr, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("添加car,参数:%s,异常:%s", reqStr, err.Error())
		return nil, errorx.NewDefaultError("添加摄像头")
	}

	return &types.AddCarsResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
