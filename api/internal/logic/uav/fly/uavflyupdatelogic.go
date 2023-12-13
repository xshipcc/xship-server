package fly

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavFlyUpdateLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavFlyUpdateLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavFlyUpdateLogic {
	return &UavFlyUpdateLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavFlyUpdateLogic) UavFlyUpdate(req *types.UpdateUavFlyReq) (resp *types.UpdateUavFlyResp, err error) {
	item, err := l.svcCtx.UavFlyModel.FindOne(l.ctx, req.Id)
	if err != nil {
		return nil, err
	}

	item.Name = req.Name
	item.Data = req.Data
	err = l.svcCtx.UavFlyModel.Update(l.ctx, item)
	if err != nil {
		return nil, err
	}

	l.svcCtx.MMQServer.Publish("control", "corn")

	return &types.UpdateUavFlyResp{
		Code:    "000000",
		Message: "保存成功",
	}, nil
}
