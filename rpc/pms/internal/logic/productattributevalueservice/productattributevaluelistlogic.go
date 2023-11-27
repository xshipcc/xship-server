package productattributevalueservicelogic

import (
	"context"
	"encoding/json"
	"zero-admin/rpc/pms/internal/svc"
	"zero-admin/rpc/pms/pmsclient"

	"github.com/zeromicro/go-zero/core/logx"
)

type ProductAttributeValueListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewProductAttributeValueListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *ProductAttributeValueListLogic {
	return &ProductAttributeValueListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *ProductAttributeValueListLogic) ProductAttributeValueList(in *pmsclient.ProductAttributeValueListReq) (*pmsclient.ProductAttributeValueListResp, error) {
	all, err := l.svcCtx.PmsProductAttributeValueModel.FindAll(l.ctx, in.ProductId)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询产品参数列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*pmsclient.ProductAttributeValueListData
	for _, item := range *all {

		list = append(list, &pmsclient.ProductAttributeValueListData{
			Id:                 item.Id,
			ProductId:          item.ProductId,
			ProductAttributeId: item.ProductAttributeId,
			Value:              item.Value.String,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询产品参数信息,参数：%s,响应：%s", reqStr, listStr)
	return &pmsclient.ProductAttributeValueListResp{
		Total: 0,
		List:  list,
	}, nil
}
