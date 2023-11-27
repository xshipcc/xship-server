package smsmodel

import (
	"context"
	"fmt"
	"github.com/zeromicro/go-zero/core/stores/sqlc"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
	"strings"
	"zero-admin/rpc/sms/smsclient"
)

var _ SmsHomeRecommendProductModel = (*customSmsHomeRecommendProductModel)(nil)

type (
	// SmsHomeRecommendProductModel is an interface to be customized, add more methods here,
	// and implement the added methods in customSmsHomeRecommendProductModel.
	SmsHomeRecommendProductModel interface {
		smsHomeRecommendProductModel
		Count(ctx context.Context, in *smsclient.HomeRecommendProductListReq) (int64, error)
		FindAll(ctx context.Context, in *smsclient.HomeRecommendProductListReq) (*[]SmsHomeRecommendProduct, error)
		FindOneByBrandId(ctx context.Context, brandId int64) (*SmsHomeRecommendProduct, error)
		DeleteByIds(ctx context.Context, ids []int64) error
	}

	customSmsHomeRecommendProductModel struct {
		*defaultSmsHomeRecommendProductModel
	}
)

// NewSmsHomeRecommendProductModel returns a model for the database table.
func NewSmsHomeRecommendProductModel(conn sqlx.SqlConn) SmsHomeRecommendProductModel {
	return &customSmsHomeRecommendProductModel{
		defaultSmsHomeRecommendProductModel: newSmsHomeRecommendProductModel(conn),
	}
}

func (m *customSmsHomeRecommendProductModel) FindAll(ctx context.Context, in *smsclient.HomeRecommendProductListReq) (*[]SmsHomeRecommendProduct, error) {

	where := "1=1"
	if len(in.ProductName) > 0 {
		where = where + fmt.Sprintf(" AND product_name like '%%%s%%'", in.ProductName)
	}
	if in.RecommendStatus != 2 {
		where = where + fmt.Sprintf(" AND recommend_status = %d", in.RecommendStatus)
	}
	query := fmt.Sprintf("select %s from %s where %s limit ?,?", smsHomeRecommendProductRows, m.table, where)
	var resp []SmsHomeRecommendProduct
	err := m.conn.QueryRows(&resp, query, (in.Current-1)*in.PageSize, in.PageSize)
	switch err {
	case nil:
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}

func (m *customSmsHomeRecommendProductModel) FindOneByBrandId(ctx context.Context, brandId int64) (*SmsHomeRecommendProduct, error) {

	where := fmt.Sprintf("product_id = %d", brandId)
	query := fmt.Sprintf("select %s from %s where %s ", smsHomeRecommendProductRows, m.table, where)
	var resp SmsHomeRecommendProduct
	err := m.conn.QueryRow(&resp, query)
	switch err {
	case nil:
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}
func (m *customSmsHomeRecommendProductModel) Count(ctx context.Context, in *smsclient.HomeRecommendProductListReq) (int64, error) {
	where := "1=1"
	if len(in.ProductName) > 0 {
		where = where + fmt.Sprintf(" AND product_name like '%%%s%%'", in.ProductName)
	}
	if in.RecommendStatus != 2 {
		where = where + fmt.Sprintf(" AND recommend_status = %d", in.RecommendStatus)
	}
	query := fmt.Sprintf("select count(*) as count from %s where %s", m.table, where)

	var count int64
	err := m.conn.QueryRow(&count, query)

	switch err {
	case nil:
		return count, nil
	case sqlc.ErrNotFound:
		return 0, ErrNotFound
	default:
		return 0, err
	}
}

func (m *customSmsHomeRecommendProductModel) DeleteByIds(ctx context.Context, ids []int64) error {
	// 拼接占位符 "?"
	placeholders := make([]string, len(ids))
	for i := range ids {
		placeholders[i] = "?"
	}

	// 构建删除语句
	query := fmt.Sprintf("DELETE FROM %s WHERE id IN (%s)", m.table, strings.Join(placeholders, ","))

	// 构建参数列表
	args := make([]interface{}, len(ids))
	for i, id := range ids {
		args[i] = id
	}

	// 执行删除语句
	_, err := m.conn.ExecCtx(ctx, query, args...)
	return err
}
