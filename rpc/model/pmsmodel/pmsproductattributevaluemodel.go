package pmsmodel

import (
	"context"
	"fmt"
	"github.com/zeromicro/go-zero/core/stores/sqlc"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
)

var _ PmsProductAttributeValueModel = (*customPmsProductAttributeValueModel)(nil)

type (
	// PmsProductAttributeValueModel is an interface to be customized, add more methods here,
	// and implement the added methods in customPmsProductAttributeValueModel.
	PmsProductAttributeValueModel interface {
		pmsProductAttributeValueModel
		FindAll(ctx context.Context, productId int64) (*[]PmsProductAttributeValue, error)
		DeleteByProductId(ctx context.Context, productId int64) error
	}

	customPmsProductAttributeValueModel struct {
		*defaultPmsProductAttributeValueModel
	}
)

// NewPmsProductAttributeValueModel returns a model for the database table.
func NewPmsProductAttributeValueModel(conn sqlx.SqlConn) PmsProductAttributeValueModel {
	return &customPmsProductAttributeValueModel{
		defaultPmsProductAttributeValueModel: newPmsProductAttributeValueModel(conn),
	}
}

func (m *customPmsProductAttributeValueModel) FindAll(ctx context.Context, productId int64) (*[]PmsProductAttributeValue, error) {

	query := fmt.Sprintf("select %s from %s where product_id =?", pmsProductAttributeValueRows, m.table)
	var resp []PmsProductAttributeValue
	err := m.conn.QueryRows(&resp, query, productId)
	switch err {
	case nil:
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}

func (m *customPmsProductAttributeValueModel) DeleteByProductId(ctx context.Context, productId int64) error {
	query := fmt.Sprintf("delete from %s where `product_id` = ?", m.table)
	_, err := m.conn.ExecCtx(ctx, query, productId)
	return err
}
