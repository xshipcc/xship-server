package uavmmqservicelogic

import (
	"context"
	"encoding/json"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavMMQListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavMMQListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavMMQListLogic {
	return &UavMMQListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 获取消息列表
func (l *UavMMQListLogic) UavMMQList(in *uavlient.UavMMQListReq) (*uavlient.UavMMQListResp, error) {
	count, _ := l.svcCtx.UavMMQModel.Count(l.ctx)
	all, err := l.svcCtx.UavMMQModel.FindAll(l.ctx, 1, count)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询MMQ信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*uavlient.UavMMQListData

	for _, fly := range *all {

		list = append(list, &uavlient.UavMMQListData{
			Id: fly.Id,
		})
	}

	return &uavlient.UavMMQListResp{
		Total: count,
		Data:  list,
	}, nil
}
