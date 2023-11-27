package people

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type PeopleUpdateLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewPeopleUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *PeopleUpdateLogic {
	return &PeopleUpdateLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *PeopleUpdateLogic) PeopleUpdate(req *types.UpdatePeopleReq) (resp *types.UpdatePeopleResp, err error) {
	item, err := l.svcCtx.UavPeopleModel.FindOne(l.ctx, req.Id)
	if err != nil {
		return nil, err
	}
	item.Level = req.Level
	item.Phone = req.Phone
	item.Status = req.Status
	item.Icon = req.Icon
	item.Gender = req.Gender
	err = l.svcCtx.UavPeopleModel.Update(l.ctx, item)
	if err != nil {
		return nil, err
	}

	return &types.UpdatePeopleResp{
		Code:    "000000",
		Message: "保存成功",
	}, nil
}
