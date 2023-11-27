package plan

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

type UavPlanAddLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavPlanAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPlanAddLogic {
	return &UavPlanAddLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavPlanAddLogic) UavPlanAdd(req *types.AddUavPlanReq) (resp *types.AddUavPlanResp, err error) {
	_, err = l.svcCtx.UavPlanModel.Insert(l.ctx, &uavmodel.UavPlan{
		UavId:      req.Uav_id,
		Plan:       req.Plan,
		FlyId:      req.Fly_id,
		CreateTime: time.Now(),
	})
	if err != nil {
		reqStr, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("添加网络失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, errorx.NewDefaultError("添加计划失败")
	}

	return &types.AddUavPlanResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
