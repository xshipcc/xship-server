package device

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

type UavDeviceAddLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewUavDeviceAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavDeviceAddLogic {
	return &UavDeviceAddLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *UavDeviceAddLogic) UavDeviceAdd(req *types.AddUavDeviceReq) (resp *types.AddUavDeviceResp, err error) {

	// _,ererr
	_, err = l.svcCtx.UavDeviceModel.Insert(l.ctx, &uavmodel.UavDevice{
		Name:        req.Name,
		Ip:          req.Ip,
		Port:        req.Port,
		RPort:       req.R_Port,
		UavZubo:     req.UavZubo,
		HangarIp:    req.Hangar_ip,
		HangarPort:  req.Hangar_port,
		HangarRport: req.Hangar_rport,
		HangarZubo:  req.HangarZubo,
		CamIp:       req.Cam_ip,
		CamPort:     req.Cam_port,
		CamUrl:      req.Cam_url,
		CamZubo:     req.CamZubo,
		CreateTime:  time.Now(),
	})

	if err != nil {
		reqStr, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("添加机构信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, errorx.NewDefaultError("添加机构失败")
	}

	return &types.AddUavDeviceResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
