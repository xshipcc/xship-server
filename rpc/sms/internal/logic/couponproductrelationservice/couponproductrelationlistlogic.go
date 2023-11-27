package couponproductrelationservicelogic

import (
	"context"
	"encoding/json"
	"zero-admin/rpc/sms/internal/svc"
	"zero-admin/rpc/sms/smsclient"

	"github.com/zeromicro/go-zero/core/logx"
)

type CouponProductRelationListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewCouponProductRelationListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *CouponProductRelationListLogic {
	return &CouponProductRelationListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *CouponProductRelationListLogic) CouponProductRelationList(in *smsclient.CouponProductRelationListReq) (*smsclient.CouponProductRelationListResp, error) {
	all, err := l.svcCtx.SmsCouponProductRelationModel.FindAll(l.ctx, in.Current, in.PageSize)
	count, _ := l.svcCtx.SmsCouponProductRelationModel.Count(l.ctx)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询优惠券与产品关糸列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*smsclient.CouponProductRelationListData
	for _, item := range *all {

		list = append(list, &smsclient.CouponProductRelationListData{
			Id:          item.Id,
			CouponId:    item.CouponId,
			ProductId:   item.ProductId,
			ProductName: item.ProductName,
			ProductSn:   item.ProductSn,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询优惠券与产品关糸列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &smsclient.CouponProductRelationListResp{
		Total: count,
		List:  list,
	}, nil
}
