package network

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

type UavNetworkAddLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavNetworkAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavNetworkAddLogic {
	return &UavNetworkAddLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavNetworkAddLogic) UavNetworkAdd(req *types.AddUavNetworkReq) (resp *types.AddUavNetworkResp, err error) {
	_, err = l.svcCtx.UavNetworkModel.Insert(l.ctx, &uavmodel.UavNetwork{
		Name:       req.Name,
		Band:       req.Band,
		CreateTime: time.Now(),
		Type:       req.Type,
	})

	if err != nil {
		reqStr, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("添加网络失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, errorx.NewDefaultError("添加网络失败")
	}

	return &types.AddUavNetworkResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
