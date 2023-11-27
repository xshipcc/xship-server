package uavmodel

import "github.com/zeromicro/go-zero/core/stores/sqlx"

var _ UavFlyHistoryDetailModel = (*customUavFlyHistoryDetailModel)(nil)

type (
	// UavFlyHistoryDetailModel is an interface to be customized, add more methods here,
	// and implement the added methods in customUavFlyHistoryDetailModel.
	UavFlyHistoryDetailModel interface {
		uavFlyHistoryDetailModel
	}

	customUavFlyHistoryDetailModel struct {
		*defaultUavFlyHistoryDetailModel
	}
)

// NewUavFlyHistoryDetailModel returns a model for the database table.
func NewUavFlyHistoryDetailModel(conn sqlx.SqlConn) UavFlyHistoryDetailModel {
	return &customUavFlyHistoryDetailModel{
		defaultUavFlyHistoryDetailModel: newUavFlyHistoryDetailModel(conn),
	}
}
