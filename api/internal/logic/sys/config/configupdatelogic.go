package logic

import (
	"context"
	"zero-admin/api/internal/common/errorx"
	"zero-admin/rpc/sys/sysclient"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type ConfigUpdateLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewConfigUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) ConfigUpdateLogic {
	return ConfigUpdateLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *ConfigUpdateLogic) ConfigUpdate(req types.UpdateConfigReq) (*types.UpdateConfigResp, error) {
	_, err := l.svcCtx.ConfigService.ConfigUpdate(l.ctx, &sysclient.ConfigUpdateReq{
		Id:           req.Id,
		Value:        req.Value,
		Label:        req.Label,
		Type:         req.Type,
		Description:  req.Description,
		Sort:         req.Sort,
		Remarks:      req.Remarks,
		LastUpdateBy: l.ctx.Value("userName").(string),
	})

	if err != nil {
		return nil, errorx.NewDefaultError("更新参数配置失败")
	}

	return &types.UpdateConfigResp{}, nil
}
