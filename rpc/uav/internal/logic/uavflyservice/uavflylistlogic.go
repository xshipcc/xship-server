package uavflyservicelogic

import (
	"context"
	"encoding/json"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavFlyListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavFlyListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavFlyListLogic {
	return &UavFlyListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 获取设备列表
func (l *UavFlyListLogic) UavFlyList(in *uavlient.UavFlyFindByIdReq) (*uavlient.ListUavFlyResp, error) {
	count, _ := l.svcCtx.UavFlyModel.Count(l.ctx)
	all, err := l.svcCtx.UavFlyModel.FindAll(l.ctx, 1, count)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询路线列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*uavlient.ListtUavFlyData

	for _, fly := range *all {

		list = append(list, &uavlient.ListtUavFlyData{
			Id:      fly.Id,
			Name:    fly.Name,
			Data:    fly.CreateTime.Format("2006-01-02 15:04:05"),
			Creator: fly.Creator,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询路线列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &uavlient.ListUavFlyResp{
		Total: count,
		List:  list,
	}, nil
}
