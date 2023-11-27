package pmsmodel

import (
	"context"
	"fmt"
	"github.com/zeromicro/go-zero/core/stores/sqlc"
	"github.com/zeromicro/go-zero/core/stores/sqlx"
	"strings"
	"zero-admin/rpc/pms/pmsclient"
)

var _ PmsBrandModel = (*customPmsBrandModel)(nil)

type (
	// PmsBrandModel is an interface to be customized, add more methods here,
	// and implement the added methods in customPmsBrandModel.
	PmsBrandModel interface {
		pmsBrandModel
		Count(ctx context.Context, in *pmsclient.BrandListReq) (int64, error)
		FindAll(ctx context.Context, in *pmsclient.BrandListReq) (*[]PmsBrand, error)
		DeleteByIds(ctx context.Context, ids []int64) error
		FindAllByIds(ctx context.Context, ids []int64) (*[]PmsBrand, error)
	}

	customPmsBrandModel struct {
		*defaultPmsBrandModel
	}
)

// NewPmsBrandModel returns a model for the database table.
func NewPmsBrandModel(conn sqlx.SqlConn) PmsBrandModel {
	return &customPmsBrandModel{
		defaultPmsBrandModel: newPmsBrandModel(conn),
	}
}

func (m *customPmsBrandModel) FindAll(ctx context.Context, in *pmsclient.BrandListReq) (*[]PmsBrand, error) {
	where := "1=1"
	if len(in.Name) > 0 {
		where = where + fmt.Sprintf(" AND name like '%%%s%%'", in.Name)
	}
	if in.FactoryStatus != 2 {
		where = where + fmt.Sprintf(" AND factory_status = '%d'", in.FactoryStatus)
	}
	if in.ShowStatus != 2 {
		where = where + fmt.Sprintf(" AND show_status = '%d'", in.ShowStatus)
	}
	query := fmt.Sprintf("select %s from %s where %s limit ?,?", pmsBrandRows, m.table, where)
	var resp []PmsBrand
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

func (m *customPmsBrandModel) Count(ctx context.Context, in *pmsclient.BrandListReq) (int64, error) {
	where := "1=1"
	if len(in.Name) > 0 {
		where = where + fmt.Sprintf(" AND name like '%%%s%%'", in.Name)
	}
	if in.FactoryStatus != 2 {
		where = where + fmt.Sprintf(" AND factory_status = '%d'", in.FactoryStatus)
	}
	if in.ShowStatus != 2 {
		where = where + fmt.Sprintf(" AND show_status = '%d'", in.ShowStatus)
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

func (m *customPmsBrandModel) DeleteByIds(ctx context.Context, ids []int64) error {
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

func (m *customPmsBrandModel) FindAllByIds(ctx context.Context, ids []int64) (*[]PmsBrand, error) {
	query := fmt.Sprintf("select %s from %s where `id` in (?)", pmsBrandRows, m.table)
	var resp []PmsBrand
	err := m.conn.QueryRows(&resp, query, strings.Replace(strings.Trim(fmt.Sprint(ids), "[]"), " ", ",", -1))
	switch err {
	case nil:
		return &resp, nil
	case sqlc.ErrNotFound:
		return nil, ErrNotFound
	default:
		return nil, err
	}
}
