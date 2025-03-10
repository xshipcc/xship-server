// Code generated by goctl. DO NOT EDIT.

package uavmodel

import (
	"context"
	"database/sql"
	"fmt"
	"strings"
	"time"

	"github.com/zeromicro/go-zero/core/stores/builder"
	"github.com/zeromicro/go-zero/core/stores/sqlc"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
	"github.com/zeromicro/go-zero/core/stringx"
)

var (
	uavPlanFieldNames          = builder.RawFieldNames(&UavPlan{})
	uavPlanRows                = strings.Join(uavPlanFieldNames, ",")
	uavPlanRowsExpectAutoSet   = strings.Join(stringx.Remove(uavPlanFieldNames, "`id`", "`create_at`", "`create_time`", "`created_at`", "`update_at`", "`update_time`", "`updated_at`"), ",")
	uavPlanRowsWithPlaceHolder = strings.Join(stringx.Remove(uavPlanFieldNames, "`id`", "`create_at`", "`create_time`", "`created_at`", "`update_at`", "`update_time`", "`updated_at`"), "=?,") + "=?"
)

type (
	uavPlanModel interface {
		Insert(ctx context.Context, data *UavPlan) (sql.Result, error)
		FindOne(ctx context.Context, id int64) (*UavPlan, error)
		Update(ctx context.Context, data *UavPlan) error
		Delete(ctx context.Context, id int64) error
	}

	defaultUavPlanModel struct {
		conn  sqlx.SqlConn
		table string
	}

	UavPlan struct {
		Id         int64     `db:"id"`          // 编号
		Name       string    `db:"name"`        // 名称
		UavId      int64     `db:"uav_id"`      // 无人机id
		UavName    string    `db:"uav_name"`    // 无人机名称
		FlyId      int64     `db:"fly_id"`      // 巡检路线id
		RoadName   string    `db:"road_name"`   // 路线名称
		Plan       string    `db:"plan"`        // 定时字符串
		Status     int64     `db:"status"`      //  帐号启用状态:0->禁用；1->启用
		CreateTime time.Time `db:"create_time"` // 飞行开始时间
	}
)

func newUavPlanModel(conn sqlx.SqlConn) *defaultUavPlanModel {
	return &defaultUavPlanModel{
		conn:  conn,
		table: "`uav_plan`",
	}
}

func (m *defaultUavPlanModel) withSession(session sqlx.Session) *defaultUavPlanModel {
	return &defaultUavPlanModel{
		conn:  sqlx.NewSqlConnFromSession(session),
		table: "`uav_plan`",
	}
}

func (m *defaultUavPlanModel) Delete(ctx context.Context, id int64) error {
	query := fmt.Sprintf("delete from %s where `id` = ?", m.table)
	_, err := m.conn.ExecCtx(ctx, query, id)
	return err
}

func (m *defaultUavPlanModel) FindOne(ctx context.Context, id int64) (*UavPlan, error) {
	query := fmt.Sprintf("select %s from %s where `id` = ? limit 1", uavPlanRows, m.table)
	var resp UavPlan
	err := m.conn.QueryRowCtx(ctx, &resp, query, id)
	switch err {
	case nil:
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}

func (m *defaultUavPlanModel) Insert(ctx context.Context, data *UavPlan) (sql.Result, error) {
	query := fmt.Sprintf("insert into %s (%s) values (?, ?, ?, ?, ?, ?, ?)", m.table, uavPlanRowsExpectAutoSet)
	ret, err := m.conn.ExecCtx(ctx, query, data.Name, data.UavId, data.UavName, data.FlyId, data.RoadName, data.Plan, data.Status)
	return ret, err
}

func (m *defaultUavPlanModel) Update(ctx context.Context, data *UavPlan) error {
	query := fmt.Sprintf("update %s set %s where `id` = ?", m.table, uavPlanRowsWithPlaceHolder)
	_, err := m.conn.ExecCtx(ctx, query, data.Name, data.UavId, data.UavName, data.FlyId, data.RoadName, data.Plan, data.Status, data.Id)
	return err
}

func (m *defaultUavPlanModel) tableName() string {
	return m.table
}
