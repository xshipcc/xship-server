package uavmodel

import (
	"context"
	"fmt"
	"strings"

	"github.com/zeromicro/go-zero/core/stores/sqlc"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
)

var _ UavPlanModel = (*customUavPlanModel)(nil)

type (
	// UavPlanModel is an interface to be customized, add more methods here,
	// and implement the added methods in customUavPlanModel.
	UavPlanModel interface {
		uavPlanModel
		Count(ctx context.Context, uav_name string, fly_name string) (int64, error)
		FindAll(ctx context.Context, uav_name string, fly_name string, Current int64, PageSize int64) (*[]UavPlan, error)
		CountActive(ctx context.Context, uav_name string, fly_name string) (int64, error)
		FindActiveAll(ctx context.Context, uav_name string, fly_name string, Current int64, PageSize int64) (*[]UavPlan, error)

		DeleteByIds(ctx context.Context, ids []int64) error
	}

	customUavPlanModel struct {
		*defaultUavPlanModel
	}
)

// NewUavPlanModel returns a model for the database table.
func NewUavPlanModel(conn sqlx.SqlConn) UavPlanModel {
	return &customUavPlanModel{
		defaultUavPlanModel: newUavPlanModel(conn),
	}
}

func (m *customUavPlanModel) FindAll(ctx context.Context, uav_name string, fly_name string, Current int64, PageSize int64) (*[]UavPlan, error) {
	where := "1=1"

	if len(uav_name) > 0 {
		where = where + fmt.Sprintf(" AND uav_name like '%%%s%%'", uav_name)
	}
	if len(fly_name) > 0 {
		where = where + fmt.Sprintf(" AND road_name like '%%%s%%'", fly_name)
	}
	query := fmt.Sprintf("select %s from %s where %s limit ?,?", uavPlanRows, m.table, where)
	var resp []UavPlan
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

func (m *customUavPlanModel) Count(ctx context.Context, uav_name string, fly_name string) (int64, error) {

	where := "1=1"

	if len(uav_name) > 0 {
		where = where + fmt.Sprintf(" AND uav_name like '%%%s%%'", uav_name)
	}
	if len(fly_name) > 0 {
		where = where + fmt.Sprintf(" AND road_name like '%%%s%%'", fly_name)
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

func (m *customUavPlanModel) FindActiveAll(ctx context.Context, uav_name string, fly_name string, Current int64, PageSize int64) (*[]UavPlan, error) {
	where := "status=1"

	if len(uav_name) > 0 {
		where = where + fmt.Sprintf(" AND uav_name like '%%%s%%'", uav_name)
	}
	if len(fly_name) > 0 {
		where = where + fmt.Sprintf(" AND road_name like '%%%s%%'", fly_name)
	}
	query := fmt.Sprintf("select %s from %s where %s limit ?,?", uavPlanRows, m.table, where)
	var resp []UavPlan
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

func (m *customUavPlanModel) CountActive(ctx context.Context, uav_name string, fly_name string) (int64, error) {

	where := "status=1"

	if len(uav_name) > 0 {
		where = where + fmt.Sprintf(" AND uav_name like '%%%s%%'", uav_name)
	}
	if len(fly_name) > 0 {
		where = where + fmt.Sprintf(" AND road_name like '%%%s%%'", fly_name)
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

func (m *customUavPlanModel) DeleteByIds(ctx context.Context, ids []int64) error {
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
