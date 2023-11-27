package uavpeopleservicelogic

import (
	"context"
	"encoding/json"

	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/logx"
)

type UavPeopleListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUavPeopleListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UavPeopleListLogic {
	return &UavPeopleListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UavPeopleListLogic) UavPeopleList(in *uavlient.ListUavPeopleReq) (*uavlient.ListUavPeopleResp, error) {
	count, _ := l.svcCtx.UavPeopleModel.Count(l.ctx)
	all, err := l.svcCtx.UavPeopleModel.FindAll(l.ctx, 1, count)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询人列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*uavlient.ListtUavPeopleData

	for _, in := range *all {

		list = append(list, &uavlient.ListtUavPeopleData{
			Id:         in.Id,
			Username:   in.Username,
			Icon:       in.Icon,
			Level:      in.Level,
			Phone:      in.Phone,
			Status:     in.Status,
			Gender:     in.Gender,
			CreateTime: in.CreateTime.Format("2006-01-02 15:04:05"),
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询人列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &uavlient.ListUavPeopleResp{
		Total: count,
		List:  list,
	}, nil
}
