package people

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type PeopleDeleteLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewPeopleDeleteLogic(ctx context.Context, svcCtx *svc.ServiceContext) *PeopleDeleteLogic {
	return &PeopleDeleteLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *PeopleDeleteLogic) PeopleDelete(req *types.DeletePeopleReq) (resp *types.DeletePeopleResp, err error) {
	err = l.svcCtx.UavPeopleModel.DeleteByIds(l.ctx, req.Ids)

	if err != nil {
		logx.WithContext(l.ctx).Errorf("删除网络失败,异常:%s", err.Error())
		return nil, err
	}
	return
}
