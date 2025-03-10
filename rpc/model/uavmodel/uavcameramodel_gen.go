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
	uavCameraFieldNames          = builder.RawFieldNames(&UavCamera{})
	uavCameraRows                = strings.Join(uavCameraFieldNames, ",")
	uavCameraRowsExpectAutoSet   = strings.Join(stringx.Remove(uavCameraFieldNames, "`id`", "`create_at`", "`create_time`", "`created_at`", "`update_at`", "`update_time`", "`updated_at`"), ",")
	uavCameraRowsWithPlaceHolder = strings.Join(stringx.Remove(uavCameraFieldNames, "`id`", "`create_at`", "`create_time`", "`created_at`", "`update_at`", "`update_time`", "`updated_at`"), "=?,") + "=?"
)

type (
	uavCameraModel interface {
		Insert(ctx context.Context, data *UavCamera) (sql.Result, error)
		FindOne(ctx context.Context, id int64) (*UavCamera, error)
		Update(ctx context.Context, data *UavCamera) error
		Delete(ctx context.Context, id int64) error
	}

	defaultUavCameraModel struct {
		conn  sqlx.SqlConn
		table string
	}

	UavCamera struct {
		Id         int64     `db:"id"`          // 摄像头id
		Name       string    `db:"name"`        // 摄像头名称
		Tunnel     int64     `db:"tunnel"`      // 通道
		Status     int64     `db:"status"`      // 状态 启用，关闭，运行，离线
		Url        string    `db:"url"`         // 摄像头地址多种信息
		RtspUrl    string    `db:"rtsp_url"`    // 摄像头AI地址
		Platform   int64     `db:"platform"`    // 使用平台：0-全部 1-飞机 2-摄像头;3-机库;4-AI;5-交通岗
		Lat        float64   `db:"lat"`         // 纬度
		Lon        float64   `db:"lon"`         // 经度
		Alt        float64   `db:"alt"`         // 高度
		AiStatus   int64     `db:"ai_status"`   //  摄像头AI 启用状态:0->禁用；1->启用
		CreateTime time.Time `db:"create_time"` // 创建时间
	}
)

func newUavCameraModel(conn sqlx.SqlConn) *defaultUavCameraModel {
	return &defaultUavCameraModel{
		conn:  conn,
		table: "`uav_camera`",
	}
}

func (m *defaultUavCameraModel) withSession(session sqlx.Session) *defaultUavCameraModel {
	return &defaultUavCameraModel{
		conn:  sqlx.NewSqlConnFromSession(session),
		table: "`uav_camera`",
	}
}

func (m *defaultUavCameraModel) Delete(ctx context.Context, id int64) error {
	query := fmt.Sprintf("delete from %s where `id` = ?", m.table)
	_, err := m.conn.ExecCtx(ctx, query, id)
	return err
}

func (m *defaultUavCameraModel) FindOne(ctx context.Context, id int64) (*UavCamera, error) {
	query := fmt.Sprintf("select %s from %s where `id` = ? limit 1", uavCameraRows, m.table)
	var resp UavCamera
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

func (m *defaultUavCameraModel) Insert(ctx context.Context, data *UavCamera) (sql.Result, error) {
	query := fmt.Sprintf("insert into %s (%s) values (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", m.table, uavCameraRowsExpectAutoSet)
	ret, err := m.conn.ExecCtx(ctx, query, data.Name, data.Tunnel, data.Status, data.Url, data.RtspUrl, data.Platform, data.Lat, data.Lon, data.Alt, data.AiStatus)
	return ret, err
}

func (m *defaultUavCameraModel) Update(ctx context.Context, data *UavCamera) error {
	query := fmt.Sprintf("update %s set %s where `id` = ?", m.table, uavCameraRowsWithPlaceHolder)
	_, err := m.conn.ExecCtx(ctx, query, data.Name, data.Tunnel, data.Status, data.Url, data.RtspUrl, data.Platform, data.Lat, data.Lon, data.Alt, data.AiStatus, data.Id)
	return err
}

func (m *defaultUavCameraModel) tableName() string {
	return m.table
}
