package device

import (
	"context"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavDeviceListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavDeviceListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavDeviceListLogic {
	return &UavDeviceListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavDeviceListLogic) UavDeviceList(req *types.ListUavDeviceReq) (resp *types.ListUavDeviceResp, err error) {
	// respList, err := l.svcCtx.UavDeviceModel.UavDeviceList(l.ctx, &uavlient.UavDeviceListReq{
	// 	Current:  req.Current,
	// 	PageSize: req.PageSize,
	// })
	count, _ := l.svcCtx.UavDeviceModel.Count(l.ctx)
	all, err := l.svcCtx.UavDeviceModel.FindAll(l.ctx, req.Current, req.PageSize)

	if err != nil {
		logx.WithContext(l.ctx).Errorf("查询无人机列表信息失败,异常:%s", err.Error())
		return nil, err
	}

	var list []*types.ListUavDeviceData

	for _, dict := range *all {
		list = append(list, &types.ListUavDeviceData{
			Id:           dict.Id,
			Name:         dict.Name,
			Ip:           dict.Ip,
			Port:         dict.Port,
			R_Port:       dict.RPort,
			Hangar_ip:    dict.HangarIp,
			Hangar_port:  dict.HangarPort,
			Hangar_rport: dict.HangarRport,
			Cam_ip:       dict.CamIp,
			Cam_port:     dict.CamPort,
			Cam_url:      dict.CamUrl,
			UavZubo:      dict.UavZubo,
			Network:      dict.Network,
			Joystick:     dict.Joystick,
			Status:       dict.Status,
		})
	}

	return &types.ListUavDeviceResp{
		Code:     "000000",
		Message:  "查询字典成功",
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    count,
	}, nil
}
