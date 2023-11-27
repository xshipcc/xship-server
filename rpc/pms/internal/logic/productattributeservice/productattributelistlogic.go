package productattributeservicelogic

import (
	"context"
	"encoding/json"
	"zero-admin/rpc/pms/internal/svc"
	"zero-admin/rpc/pms/pmsclient"

	"github.com/zeromicro/go-zero/core/logx"
)

type ProductAttributeListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewProductAttributeListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *ProductAttributeListLogic {
	return &ProductAttributeListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *ProductAttributeListLogic) ProductAttributeList(in *pmsclient.ProductAttributeListReq) (*pmsclient.ProductAttributeListResp, error) {
	all, err := l.svcCtx.PmsProductAttributeModel.FindAll(l.ctx, in)
	count, _ := l.svcCtx.PmsProductAttributeModel.Count(l.ctx, in)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询商品属性列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*pmsclient.ProductAttributeListData
	for _, item := range *all {

		list = append(list, &pmsclient.ProductAttributeListData{
			Id:                         item.Id,
			ProductAttributeCategoryId: item.ProductAttributeCategoryId,
			Name:                       item.Name,
			SelectType:                 item.SelectType,
			InputType:                  item.InputType,
			InputList:                  item.InputList,
			Sort:                       item.Sort,
			FilterType:                 item.FilterType,
			SearchType:                 item.SearchType,
			RelatedStatus:              item.RelatedStatus,
			HandAddStatus:              item.HandAddStatus,
			Type:                       item.Type,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询商品属性列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &pmsclient.ProductAttributeListResp{
		Total: count,
		List:  list,
	}, nil
}
