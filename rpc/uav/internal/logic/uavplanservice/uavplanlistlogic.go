package uavplanservicelogic

import (
	"context"
	"encoding/json"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPlanListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavPlanListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPlanListLogic {
	return &UavPlanListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavPlanListLogic) UavPlanList(in *uavlient.ListUavPlanReq) (*uavlient.ListUavPlanResp, error) {
	count, _ := l.svcCtx.UavPlanModel.Count(l.ctx)
	all, err := l.svcCtx.UavPlanModel.FindAll(l.ctx, 1, count)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询计划列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*uavlient.ListtUavPlanData

	for _, in := range *all {

		list = append(list, &uavlient.ListtUavPlanData{
			Id:         in.Id,
			UavId:      in.UavId,
			Plan:       in.Plan,
			FlyId:      in.FlyId,
			CreateTime: in.CreateTime.Format("2006-01-02 15:04:05"),
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询计划表信息,参数：%s,响应：%s", reqStr, listStr)
	return &uavlient.ListUavPlanResp{
		Total: count,
		List:  list,
	}, nil
}
