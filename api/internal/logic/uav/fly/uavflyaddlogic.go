package fly

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

type UavFlyAddLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavFlyAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavFlyAddLogic {
	return &UavFlyAddLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavFlyAddLogic) UavFlyAdd(req *types.AddUavFlyReq) (resp *types.AddUavFlyResp, err error) {

	_, err = l.svcCtx.UavFlyModel.Insert(l.ctx, &uavmodel.UavFly{
		Name:       req.Name,
		Data:       req.Data,
		CreateTime: time.Now(),
		Creator:    req.Creator,
	})
	if err != nil {
		reqStr, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("添加航线失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, errorx.NewDefaultError("添加航线失败")
	}

	l.svcCtx.MMQServer.Publish("control", "corn")

	return &types.AddUavFlyResp{
		Code:    "000000",
		Message: "111",
	}, nil

}
