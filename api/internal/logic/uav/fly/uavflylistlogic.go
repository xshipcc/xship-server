package fly

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavFlyListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavFlyListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavFlyListLogic {
	return &UavFlyListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavFlyListLogic) UavFlyList(req *types.ListUavFlyReq) (resp *types.ListUavFlyResp, err error) {
	count, _ := l.svcCtx.UavFlyModel.Count(l.ctx, req.Id)
	all, err := l.svcCtx.UavFlyModel.FindAll(l.ctx, req.Id, req.Current, req.PageSize)

	if err != nil {
		data, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("参数: %s,查询飞行路线异常:%s", string(data), err.Error())
		return nil, errorx.NewDefaultError("查询飞行路线失败")
	}
	var list []*types.ListUavFlyData

	for _, dict := range *all {
		list = append(list, &types.ListUavFlyData{
			Id:         dict.Id,
			Name:       dict.Name,
			Data:       dict.Data,
			CreateTime: dict.CreateTime.Format("2006-01-02 15:04:05"),
			Creator:    dict.Creator,
		})
	}

	return &types.ListUavFlyResp{
		Code:     "000000",
		Message:  "查询字典成功",
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    count,
	}, nil
}
