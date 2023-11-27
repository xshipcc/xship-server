package attribute

import (
	"context"
	"encoding/json"
	"zero-admin/api/internal/common/errorx"
	"zero-admin/rpc/pms/pmsclient"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type ProductAttributeListLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewProductAttributeListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *ProductAttributeListLogic {
	return &ProductAttributeListLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *ProductAttributeListLogic) ProductAttributeList(req *types.ListProductAttributeReq) (resp *types.ListProductAttributeResp, err error) {
	attributeList, er := l.svcCtx.ProductAttributeService.ProductAttributeList(l.ctx, &pmsclient.ProductAttributeListReq{
		Current:                    req.Current,
		PageSize:                   req.PageSize,
		Name:                       req.Name,
		Type:                       req.Type,
		ProductAttributeCategoryId: req.ProductAttributeCategoryId,
	})

	if er != nil {
		data, _ := json.Marshal(req)
		logx.WithContext(l.ctx).Errorf("参数: %s,查询属性列表异常:%s", string(data), er.Error())
		return nil, errorx.NewDefaultError("查询属性失败")
	}

	var list []*types.ListtProductAttributeData

	for _, item := range attributeList.List {
		list = append(list, &types.ListtProductAttributeData{
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

	return &types.ListProductAttributeResp{
		Current:  req.Current,
		Data:     list,
		PageSize: req.PageSize,
		Success:  true,
		Total:    attributeList.Total,
		Code:     "000000",
		Message:  "查询属性成功",
	}, nil
}
