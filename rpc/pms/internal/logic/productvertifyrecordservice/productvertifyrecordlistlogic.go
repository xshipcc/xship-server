package productvertifyrecordservicelogic

import (
	"context"
	"encoding/json"
	"zero-admin/rpc/pms/internal/svc"
	"zero-admin/rpc/pms/pmsclient"

	"github.com/zeromicro/go-zero/core/logx"
)

type ProductVertifyRecordListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewProductVertifyRecordListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *ProductVertifyRecordListLogic {
	return &ProductVertifyRecordListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *ProductVertifyRecordListLogic) ProductVertifyRecordList(in *pmsclient.ProductVertifyRecordListReq) (*pmsclient.ProductVertifyRecordListResp, error) {
	all, err := l.svcCtx.PmsProductVertifyRecordModel.FindAll(l.ctx, in.Current, in.PageSize)
	count, _ := l.svcCtx.PmsProductVertifyRecordModel.Count(l.ctx)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询商品审核列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*pmsclient.ProductVertifyRecordListData
	for _, item := range *all {

		list = append(list, &pmsclient.ProductVertifyRecordListData{
			Id:         item.Id,
			ProductId:  item.ProductId,
			CreateTime: item.CreateTime.Format("2006-01-02 15:04:05"),
			VertifyMan: item.VertifyMan,
			Status:     item.Status,
			Detail:     item.Detail,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询商品审核列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &pmsclient.ProductVertifyRecordListResp{
		Total: count,
		List:  list,
	}, nil
}
