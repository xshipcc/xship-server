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
		/*
				// Type        int64  `json:"type"`//'消息类型:0-全部 1-巡检路线 2-入侵 3-烟火 4-人员 5-车辆',
			// 	Platform    int64  `json:"platform"` //监控的平台 '使用平台：0-全部 1-飞机 2-摄像头;3-机库;4-AI',
			// 	HistoryID 	int64  `json:"history_id"`// 巡检路线id 告警信息和巡检路线id绑定 巡检路线->告警路线 一对多
			// 	Confirm       int64  `json:"confirm"`//是否是 审查过的。*/

		Count(ctx context.Context, history_type int64, day string, platform int64, history_id int64, confirm int64) (int64, error)
		FindAll(ctx context.Context, history_type int64, day string, platform int64, history_id int64, confirm int64, Current int64, PageSize int64) (*[]UavMessage, error)
		FindCount(ctx context.Context, history_type int64, day string, count int64) (*[]UavMessage, error)
		AleretCount(ctx context.Context, date string, stauts int) (*[]UavMessage, error)
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

func (m *customUavMessageModel) AleretCount(ctx context.Context, date string, stauts int) (*[]UavMessage, error) {
	query := fmt.Sprintf("select type, COUNT(*) AS count from %s where DATE(create_time) = %s GROUP BY type", m.table, date)
	var resp []UavMessage
	if stauts >= 0 {
		query = fmt.Sprintf("select type, COUNT(*) AS count from %s where DATE(create_time) = %s AND confirm = %d GROUP BY type", m.table, date, stauts)
	}

	// var count int64
	type Result struct {
		Type  int64
		Count int64
	}

	var results []Result
	// res, err := m.conn.Exec(query)

	err := m.conn.QueryRows(&results, query)

	switch err {
	case nil:
		for _, dict := range results {
			fmt.Printf("%d : %d", dict.Type, dict.Count)

			resp = append(resp, UavMessage{
				Type:  dict.Type,
				Count: dict.Count,
			})
		}
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}

func (m *customUavMessageModel) FindAll(ctx context.Context, history_type int64, day string, platform int64, history_id int64, confirm int64, Current int64, PageSize int64) (*[]UavMessage, error) {

	where := "1=1"

	if history_id > 0 {
		where = where + fmt.Sprintf(" AND history_id = %d ", history_id)
	}

	if history_type > 0 {
		where = where + fmt.Sprintf(" AND type = %d", history_type)
	}
	if platform > 0 {
		where = where + fmt.Sprintf(" AND platform = %d", platform)
	}
	if confirm > 0 {
		where = where + fmt.Sprintf(" AND confirm = %d", confirm)
	}
	if len(day) > 0 {
		where = where + fmt.Sprintf(" AND create_time BETWEEN '%s 00:00:00' AND '%s 23:59:59'", day, day)
	}
	where = where + "  ORDER BY create_time DESC"
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

func (m *customUavMessageModel) FindCount(ctx context.Context, history_type int64, day string, count int64) (*[]UavMessage, error) {

	where := "1=1"
	if history_type > 0 {
		where = where + fmt.Sprintf(" AND type = %d", history_type)
	}

	where = where + fmt.Sprintf(" AND create_time BETWEEN '%s 00:00:00' AND '%s 23:59:59'", day, day)

	query := fmt.Sprintf("select %s from %s where %s limit ?,?", uavMessageRows, m.table, where)
	var resp []UavMessage
	err := m.conn.QueryRows(&resp, query, 0, count)
	switch err {
	case nil:
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}

func (m *customUavMessageModel) Count(ctx context.Context, history_type int64, day string, platform int64, history_id int64, confirm int64) (int64, error) {
	where := "1=1"

	if history_id > 0 {
		where = where + fmt.Sprintf(" AND history_id = %d", history_id)
	}
	if history_type > 0 {
		where = where + fmt.Sprintf(" AND type = %d", history_type)
	}
	if platform > 0 {
		where = where + fmt.Sprintf(" AND platform = %d", platform)
	}
	if confirm > 0 {
		where = where + fmt.Sprintf(" AND confirm = %d", confirm)
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
