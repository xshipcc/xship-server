package people

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

type PeopleAddLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewPeopleAddLogic(ctx context.Context, svcCtx *svc.ServiceContext) *PeopleAddLogic {
	return &PeopleAddLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l PeopleAddLogic) PeopleAdd(req *types.AddPeopleReq) (resp *types.AddPeopleResp, err error) {
	_, err = l.svcCtx.UavPeopleModel.Insert(l.ctx, &uavmodel.UavPeople{
		Username:   req.Username,
		Icon:       req.Icon,
		Level:      req.Level,
		Phone:      req.Phone,
		Status:     req.Status,
		Gender:     req.Gender,
		CreateTime: time.Now(),
	})

	if err != nil {
		reqStr, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("添加网络失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, errorx.NewDefaultError("添加人员失败")
	}

	return &types.AddPeopleResp{
		Code:    "000000",
		Message: "111",
	}, nil
}
