package mmqmodel

import (
	"context"
	"fmt"

	"github.com/zeromicro/go-zero/core/stores/sqlc"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
)

var _ MmqMessageModel = (*customMmqMessageModel)(nil)

type (
	// MmqMessageModel is an interface to be customized, add more methods here,
	// and implement the added methods in customMmqMessageModel.
	MmqMessageModel interface {
		mmqMessageModel
		Count(ctx context.Context) (int64, error)
		FindAll(ctx context.Context, Current int64, PageSize int64) (*[]MmqMessage, error)
	}

	customMmqMessageModel struct {
		*defaultMmqMessageModel
	}
)

// NewMmqMessageModel returns a model for the database table.
func NewMmqMessageModel(conn sqlx.SqlConn) MmqMessageModel {
	return &customMmqMessageModel{
		defaultMmqMessageModel: newMmqMessageModel(conn),
	}
}

func (m *customMmqMessageModel) FindAll(ctx context.Context, Current int64, PageSize int64) (*[]MmqMessage, error) {

	query := fmt.Sprintf("select %s from %s limit ?,?", mmqMessageRows, m.table)
	var resp []MmqMessage
	err := m.conn.QueryRows(&resp, query, (Current-1)*PageSize, PageSize)
	switch err {
	case nil:
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}

func (m *customMmqMessageModel) Count(ctx context.Context) (int64, error) {
	query := fmt.Sprintf("select count(*) as count from %s", m.table)

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
