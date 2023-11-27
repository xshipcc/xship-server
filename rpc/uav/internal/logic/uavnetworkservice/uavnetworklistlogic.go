package uavnetworkservicelogic

import (
	"context"
	"encoding/json"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavNetworkListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavNetworkListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavNetworkListLogic {
	return &UavNetworkListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavNetworkListLogic) UavNetworkList(in *uavlient.ListUavNetworkReq) (*uavlient.ListUavNetworkResp, error) {
	count, _ := l.svcCtx.UavNetworkModel.Count(l.ctx)
	all, err := l.svcCtx.UavNetworkModel.FindAll(l.ctx, 1, count)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询网络列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*uavlient.ListtUavNetworkData

	for _, net := range *all {

		list = append(list, &uavlient.ListtUavNetworkData{
			Id:   net.Id,
			Name: net.Name,
			Band: net.Band,
			Type: net.Type,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询网络列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &uavlient.ListUavNetworkResp{
		Total: count,
		List:  list,
	}, nil
}
