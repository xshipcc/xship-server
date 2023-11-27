package network

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavNetworkListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavNetworkListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavNetworkListLogic {
	return &UavNetworkListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavNetworkListLogic) UavNetworkList(req *types.ListUavNetworkReq) (resp *types.ListUavNetworkResp, err error) {
	count, _ := l.svcCtx.UavNetworkModel.Count(l.ctx)
	all, err := l.svcCtx.UavNetworkModel.FindAll(l.ctx, req.Current, req.PageSize)

	if err != nil {
		data, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("参数: %s,查询网络列表异常:%s", string(data), err.Error())
		return nil, errorx.NewDefaultError("查询网络失败")
	}
	var list []*types.ListtUavNetworkData

	for _, dict := range *all {
		list = append(list, &types.ListtUavNetworkData{
			Id:   dict.Id,
			Name: dict.Name,
			Band: dict.Band,
			Type: dict.Type,
		})
	}

	return &types.ListUavNetworkResp{
		Code:     "000000",
		Message:  "查询字典成功",
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    count,
	}, nil
}
