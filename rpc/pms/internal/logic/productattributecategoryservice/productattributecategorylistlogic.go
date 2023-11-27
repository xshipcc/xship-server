package productattributecategoryservicelogic

import (
	"context"
	"encoding/json"
	"zero-admin/rpc/pms/internal/svc"
	"zero-admin/rpc/pms/pmsclient"

	"github.com/zeromicro/go-zero/core/logx"
)

type ProductAttributeCategoryListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewProductAttributeCategoryListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *ProductAttributeCategoryListLogic {
	return &ProductAttributeCategoryListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *ProductAttributeCategoryListLogic) ProductAttributeCategoryList(in *pmsclient.ProductAttributeCategoryListReq) (*pmsclient.ProductAttributeCategoryListResp, error) {
	all, err := l.svcCtx.PmsProductAttributeCategoryModel.FindAll(l.ctx, in)
	count, _ := l.svcCtx.PmsProductAttributeCategoryModel.Count(l.ctx, in)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询商品属性类别列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*pmsclient.ProductAttributeCategoryListData
	for _, item := range *all {

		list = append(list, &pmsclient.ProductAttributeCategoryListData{
			Id:             item.Id,
			Name:           item.Name,
			AttributeCount: item.AttributeCount,
			ParamCount:     item.ParamCount,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询商品属性类别列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &pmsclient.ProductAttributeCategoryListResp{
		Total: count,
		List:  list,
	}, nil
}
