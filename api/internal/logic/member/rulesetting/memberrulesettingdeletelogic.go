package logic

import (
	"context"
	"zero-admin/api/internal/common/errorx"
	"zero-admin/rpc/ums/umsclient"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type MemberRuleSettingDeleteLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewMemberRuleSettingDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) MemberRuleSettingDeleteLogic {
	return MemberRuleSettingDeleteLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *MemberRuleSettingDeleteLogic) MemberRuleSettingDelete(req types.DeleteMemberRuleSettingReq) (*types.DeleteMemberRuleSettingResp, error) {
	_, err := l.svcCtx.MemberRuleSettingService.MemberRuleSettingDelete(l.ctx, &umsclient.MemberRuleSettingDeleteReq{
		Ids: req.Ids,
	})

	if err != nil {
		logx.WithContext(l.ctx).Errorf("根据Id: %d,删除积分规则异常:%s", req.Ids, err.Error())
		return nil, errorx.NewDefaultError("删除积分规则失败")
	}
	return &types.DeleteMemberRuleSettingResp{
		Code:    "000000",
		Message: "",
	}, nil
}
