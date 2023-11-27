package people

import (
	"context"
	"encoding/json"

	"zero-admin/api/internal/common/errorx"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type PeopleListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewPeopleListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *PeopleListLogic {
	return &PeopleListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *PeopleListLogic) PeopleList(req *types.ListPeopleReq) (resp *types.ListPeopleResp, err error) {
	count, _ := l.svcCtx.UavPeopleModel.Count(l.ctx)
	all, err := l.svcCtx.UavPeopleModel.FindAll(l.ctx, req.Current, req.PageSize)

	if err != nil {
		data, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("参数: %s,查询人员列表异常:%s", string(data), err.Error())
		return nil, errorx.NewDefaultError("查询字典失败")
	}
	var list []*types.ListtPeopleData

	for _, dict := range *all {
		list = append(list, &types.ListtPeopleData{
			Id:         dict.Id,
			Level:      dict.Level,
			Username:   dict.Username,
			Phone:      dict.Phone,
			Status:     dict.Status,
			Icon:       dict.Icon,
			Gender:     dict.Gender,
			CreateTime: dict.CreateTime.Format("2006-01-02 15:04:05"),
		})
	}

	return &types.ListPeopleResp{
		Code:     "000000",
		Message:  "查询字典成功",
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    count,
	}, nil
}
