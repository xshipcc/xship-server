package uavmodel

import (
	"context"
	"fmt"
	"strings"

	"github.com/zeromicro/go-zero/core/stores/sqlc"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
)

var _ UavDeviceModel = (*customUavDeviceModel)(nil)

type (
	// UavDeviceModel is an interface to be customized, add more methods here,
	// and implement the added methods in customUavDeviceModel.
	UavDeviceModel interface {
		uavDeviceModel
		/*
			Id          int64  `json:"id"`
			Status  int64      `json:"status"`
			UavZubo    int64   `json:"uav_zubo"`
		*/
		Count(ctx context.Context, id int64, status int64, zubo int64) (int64, error)
		FindAll(ctx context.Context, id int64, status int64, zubo int64, Current int64, PageSize int64) (*[]UavDevice, error)
		FindOneActive(ctx context.Context) (*UavDevice, error)
		DeleteByIds(ctx context.Context, ids []int64) error
	}

	customUavDeviceModel struct {
		*defaultUavDeviceModel
	}
)

// NewUavDeviceModel returns a model for the database table.
func NewUavDeviceModel(conn sqlx.SqlConn) UavDeviceModel {
	return &customUavDeviceModel{
		defaultUavDeviceModel: newUavDeviceModel(conn),
	}
}

func (m *customUavDeviceModel) FindAll(ctx context.Context, id int64, status int64, zubo int64, Current int64, PageSize int64) (*[]UavDevice, error) {

	where := "1=1"

	if id > 0 {
		where = where + fmt.Sprintf(" AND id = %d ", id)
	}
	if status > 0 {
		where = where + fmt.Sprintf(" AND status = %d", status)
	}
	if zubo > 0 {
		where = where + fmt.Sprintf(" AND type = %d", zubo)
	}
	query := fmt.Sprintf("select %s from %s where %s limit ?,?", uavDeviceRows, m.table, where)

	// query := fmt.Sprintf("select %s from %s limit ?,?", uavDeviceRows, m.table)
	var resp []UavDevice
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

func (m *customUavDeviceModel) FindOneActive(ctx context.Context) (*UavDevice, error) {

	query := fmt.Sprintf("select %s from %s where `status` = ? limit 1", uavDeviceRows, m.table)
	var resp UavDevice
	err := m.conn.QueryRowCtx(ctx, &resp, query, 1)
	switch err {
	case nil:
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}

func (m *customUavDeviceModel) Count(ctx context.Context, id int64, status int64, zubo int64) (int64, error) {

	where := "1=1"

	if id > 0 {
		where = where + fmt.Sprintf(" AND id = %d ", id)
	}
	if status > 0 {
		where = where + fmt.Sprintf(" AND status = %d", status)
	}
	if zubo > 0 {
		where = where + fmt.Sprintf(" AND type = %d", zubo)
	}
	query := fmt.Sprintf("select count(*) as count from %s where %s", m.table, where)
	// query := fmt.Sprintf("select count(*) as count from %s", m.table)

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

func (m *customUavDeviceModel) DeleteByIds(ctx context.Context, ids []int64) error {
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
