package uavhistoryservicelogic

import (
	"context"
	"encoding/json"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavHistoryListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavHistoryListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavHistoryListLogic {
	return &UavHistoryListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavHistoryListLogic) UavHistoryList(in *uavlient.ListUavHistoryReq) (*uavlient.ListUavHistoryResp, error) {
	// todo: add your logic here and delete this line
	count, _ := l.svcCtx.UavFlyHistoryModel.Count(l.ctx)
	all, err := l.svcCtx.UavFlyHistoryModel.FindAll(l.ctx, 1, count)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询无人机历史信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*uavlient.ListtUavHistoryData

	for _, fly := range *all {

		list = append(list, &uavlient.ListtUavHistoryData{
			Id:         fly.Id,
			UavId:      fly.UavId,
			FlyID:      fly.FlyId,
			Operator:   fly.Operator,
			CreateTime: fly.CreateTime.Format("2006-01-02 15:04:05"),
			EndTime:    fly.EndTime.Format("2006-01-02 15:04:05"),
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询无人机列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &uavlient.ListUavHistoryResp{
		Total: count,
		List:  list,
	}, nil
}
