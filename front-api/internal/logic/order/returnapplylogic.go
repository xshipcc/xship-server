package order

import (
	"context"
	"zero-admin/rpc/oms/omsclient"

	"zero-admin/front-api/internal/svc"
	"zero-admin/front-api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type ReturnApplyLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
}

func NewReturnApplyLogic(ctx context.Context, svcCtx *svc.ServiceContext) *ReturnApplyLogic {
	return &ReturnApplyLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
	}
}

func (l *ReturnApplyLogic) ReturnApply(req *types.ReturnApplyReq) (resp *types.ReturnApplyResp, err error) {
	_, err = l.svcCtx.OrderReturnApplyService.OrderReturnApplyAdd(l.ctx, &omsclient.OrderReturnApplyAddReq{
		OrderId:          req.OrderID,
		ProductId:        req.ProductID,
		OrderSn:          req.OrderSn,
		MemberUsername:   req.MemberUsername,
		ReturnName:       req.ReturnName,
		ReturnPhone:      req.ReturnPhone,
		Status:           0,
		ProductPic:       req.ProductPic,
		ProductName:      req.ProductName,
		ProductBrand:     req.ProductBrand,
		ProductAttr:      req.ProductAttr,
		ProductCount:     req.ProductCount,
		ProductPrice:     req.ProductPrice,
		ProductRealPrice: req.ProductRealPrice,
		Reason:           req.Reason,
		Description:      req.Description,
		ProofPics:        req.ProofPics,
	})
	if err != nil {
		return nil, err
	}

	return &types.ReturnApplyResp{
		Code:    0,
		Message: "操作成功",
	}, nil
}
