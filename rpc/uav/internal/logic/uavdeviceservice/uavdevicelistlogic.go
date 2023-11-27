package uavdeviceservicelogic

import (
	"context"
	"encoding/json"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavDeviceListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavDeviceListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavDeviceListLogic {
	return &UavDeviceListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

// 获取设备列表
func (l *UavDeviceListLogic) UavDeviceList(in *uavlient.UavDeviceListReq) (*uavlient.UavDeviceListResp, error) {
	count, _ := l.svcCtx.UavDeviceModel.Count(l.ctx)
	all, err := l.svcCtx.UavDeviceModel.FindAll(l.ctx, in.Current, in.PageSize)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询无人机列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*uavlient.UavDeviceListData

	for _, devinfo := range *all {

		list = append(list, &uavlient.UavDeviceListData{
			Id:         devinfo.Id,
			Name:       devinfo.Name,
			Ip:         devinfo.Ip,
			Port:       devinfo.Port,
			HangarIp:   devinfo.HangarIp,
			HangarPort: devinfo.HangarPort,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询无人机设备列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &uavlient.UavDeviceListResp{
		Total: count,
		Data:  list,
	}, nil
}
