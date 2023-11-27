package homerecommendsubjectservicelogic

import (
	"context"
	"encoding/json"
	"zero-admin/rpc/sms/internal/svc"
	"zero-admin/rpc/sms/smsclient"

	"github.com/zeromicro/go-zero/core/logx"
)

type HomeRecommendSubjectListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewHomeRecommendSubjectListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *HomeRecommendSubjectListLogic {
	return &HomeRecommendSubjectListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *HomeRecommendSubjectListLogic) HomeRecommendSubjectList(in *smsclient.HomeRecommendSubjectListReq) (*smsclient.HomeRecommendSubjectListResp, error) {
	all, err := l.svcCtx.SmsHomeRecommendSubjectModel.FindAll(l.ctx, in)
	count, _ := l.svcCtx.SmsHomeRecommendSubjectModel.Count(l.ctx, in)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询人气专题推荐列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*smsclient.HomeRecommendSubjectListData
	for _, item := range *all {

		list = append(list, &smsclient.HomeRecommendSubjectListData{
			Id:              item.Id,
			SubjectId:       item.SubjectId,
			SubjectName:     item.SubjectName,
			RecommendStatus: item.RecommendStatus,
			Sort:            item.Sort,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询人气专题推荐列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &smsclient.HomeRecommendSubjectListResp{
		Total: count,
		List:  list,
	}, nil
}
