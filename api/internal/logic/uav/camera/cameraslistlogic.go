package camera

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type CamerasListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewCamerasListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *CamerasListLogic {
	return &CamerasListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *CamerasListLogic) CamerasList(req *types.ListCamerasReq) (resp *types.ListCamerasResp, err error) {
	count, _ := l.svcCtx.UavCameraModel.Count(l.ctx)
	all, err := l.svcCtx.UavCameraModel.FindAll(l.ctx, req.Current, req.PageSize)

	if err != nil {
		data, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("参数: %s,查询飞行路线异常:%s", string(data), err.Error())
		return nil, errorx.NewDefaultError("查询飞行路线失败")
	}
	var list []*types.ListCamerasData

	for _, dict := range *all {
		list = append(list, &types.ListCamerasData{
			Id:        dict.Id,
			Name:      dict.Name,
			Tunnel:    dict.Tunnel,
			Status:    dict.Status,
			Url:       dict.Url,
			Platform:  dict.Platform,
			Lat:       dict.Lat,
			Lon:       dict.Lon,
			Alt:       dict.Alt,
			Ai_status: dict.AiStatus,
		})
	}

	return &types.ListCamerasResp{
		Code:     "000000",
		Message:  "查询字典成功",
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    count,
	}, nil
}
