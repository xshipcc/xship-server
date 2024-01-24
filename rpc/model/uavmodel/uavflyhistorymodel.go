package uavmodel

import (
	"context"
	"fmt"

	"github.com/zeromicro/go-zero/core/stores/sqlc"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
)

var _ UavFlyHistoryModel = (*customUavFlyHistoryModel)(nil)

type (
	// UavFlyHistoryModel is an interface to be customized, add more methods here,
	// and implement the added methods in customUavFlyHistoryModel.
	UavFlyHistoryModel interface {
		uavFlyHistoryModel
		Count(ctx context.Context, history_id int64, status int64, day string) (int64, error)
		CountStatus(ctx context.Context, staus int64) (int64, error)

		FindAll(ctx context.Context, history_id int64, status int64, day string, Current int64, PageSize int64) (*[]UavFlyHistory, error)
	}

	customUavFlyHistoryModel struct {
		*defaultUavFlyHistoryModel
	}
)

// NewUavFlyHistoryModel returns a model for the database table.
func NewUavFlyHistoryModel(conn sqlx.SqlConn) UavFlyHistoryModel {
	return &customUavFlyHistoryModel{
		defaultUavFlyHistoryModel: newUavFlyHistoryModel(conn),
	}
}

func (m *customUavFlyHistoryModel) FindAll(ctx context.Context, history_id int64, status int64, day string, Current int64, PageSize int64) (*[]UavFlyHistory, error) {
	where := "1=1"

	if history_id > 0 {
		where = where + fmt.Sprintf(" AND id = %d ", history_id)
	}
	if status >= 0 {
		where = where + fmt.Sprintf(" AND status = %d", status)
	}

	if len(day) > 0 {
		where = where + fmt.Sprintf(" AND create_time BETWEEN '%s 00:00:00' AND '%s 23:59:59'", day, day)
	}
	where = where + fmt.Sprint(" ORDER BY create_time DESC")
	query := fmt.Sprintf("select %s from %s where %s limit ?,?", uavFlyHistoryRows, m.table, where)
	var resp []UavFlyHistory
	// err := m.conn.QueryRows(&resp, query, (in.Current-1)*in.PageSize, in.PageSize)
	// query := fmt.Sprintf("select %s from %s limit ?,?", uavFlyHistoryRows, m.table)
	// var resp []UavFlyHistory
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

func (m *customUavFlyHistoryModel) CountStatus(ctx context.Context, staus int64) (int64, error) {
	where := "1=1"

	if staus >= 0 {
		where = where + fmt.Sprintf(" AND staus = %d", staus)
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

func (m *customUavFlyHistoryModel) Count(ctx context.Context, history_id int64, status int64, day string) (int64, error) {
	where := "1=1"

	if history_id > 0 {
		where = where + fmt.Sprintf(" AND id = %d", history_id)
	}

	if status >= 0 {
		where = where + fmt.Sprintf(" AND status = %d", status)
	}

	if len(day) > 0 {
		where = where + fmt.Sprintf(" AND create_time BETWEEN '%s 00:00:00' AND '%s 23:59:59'", day, day)
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
