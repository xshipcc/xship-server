package subjectservicelogic

import (
	"context"

	"zero-admin/rpc/cms/cmsclient"
	"zero-admin/rpc/cms/internal/svc"

	"github.com/zeromicro/go-zero/core/logx"
)

type SubjectUpdateLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewSubjectUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *SubjectUpdateLogic {
	return &SubjectUpdateLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *SubjectUpdateLogic) SubjectUpdate(in *cmsclient.SubjectUpdateReq) (*cmsclient.SubjectUpdateResp, error) {
	// todo: add your logic here and delete this line

	return &cmsclient.SubjectUpdateResp{}, nil
}
