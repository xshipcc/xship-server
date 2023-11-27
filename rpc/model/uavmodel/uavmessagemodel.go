package uavmodel

import (
	"context"
	"fmt"
	"strings"

	"github.com/zeromicro/go-zero/core/stores/sqlc"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
)

var _ UavMessageModel = (*customUavMessageModel)(nil)

type (
	// UavMessageModel is an interface to be customized, add more methods here,
	// and implement the added methods in customUavMessageModel.
	UavMessageModel interface {
		uavMessageModel
		Count(ctx context.Context, history_id int64) (int64, error)
		FindAll(ctx context.Context, history_id int64, Current int64, PageSize int64) (*[]UavMessage, error)
	}

	customUavMessageModel struct {
		*defaultUavMessageModel
	}
)

// NewUavMessageModel returns a model for the database table.
func NewUavMessageModel(conn sqlx.SqlConn) UavMessageModel {
	return &customUavMessageModel{
		defaultUavMessageModel: newUavMessageModel(conn),
	}
}

func (m *customUavMessageModel) FindAll(ctx context.Context, history_id int64, Current int64, PageSize int64) (*[]UavMessage, error) {

	where := "1=1"

	if history_id > 0 {
		where = where + fmt.Sprintf(" AND history_id = %d ", history_id)
	}
	query := fmt.Sprintf("select %s from %s where %s limit ?,?", uavMessageRows, m.table, where)

	var resp []UavMessage
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

func (m *customUavMessageModel) Count(ctx context.Context, history_id int64) (int64, error) {
	where := "1=1"

	if history_id > 0 {
		where = where + fmt.Sprintf(" AND history_id = %d", history_id)
	}
	query := fmt.Sprintf("select count(*) as count from %s where %s ", m.table, where)

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

func (m *customUavMessageModel) DeleteByIds(ctx context.Context, ids []int64) error {
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
