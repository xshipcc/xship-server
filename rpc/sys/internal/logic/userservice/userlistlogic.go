package userservicelogic

import (
	"context"
	"encoding/json"
	"github.com/zeromicro/go-zero/core/logx"
	"zero-admin/rpc/sys/internal/svc"
	"zero-admin/rpc/sys/sysclient"
)

type UserListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewUserListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *UserListLogic {
	return &UserListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *UserListLogic) UserList(in *sysclient.UserListReq) (*sysclient.UserListResp, error) {

	all, err := l.svcCtx.UserModel.FindAll(l.ctx, in)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询用户列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	count, _ := l.svcCtx.UserModel.Count(l.ctx, in)

	var list []*sysclient.UserListData
	for _, user := range *all {
		list = append(list, &sysclient.UserListData{
			Id:             user.Id,
			Name:           user.Name,
			NickName:       user.NickName.String,
			Avatar:         user.Avatar.String,
			Email:          user.Email.String,
			Mobile:         user.Mobile.String,
			DeptId:         user.DeptId,
			Status:         user.Status,
			CreateBy:       user.CreateBy,
			CreateTime:     user.CreateTime.Format("2006-01-02 15:04:05"),
			LastUpdateBy:   user.UpdateBy.String,
			LastUpdateTime: user.UpdateTime.Time.Format("2006-01-02 15:04:05"),
			DelFlag:        user.DelFlag,
			JobId:          user.JobId,
			RoleId:         user.RoleId,
			RoleName:       user.RoleName,
			JobName:        user.JobName,
			DeptName:       user.DeptName,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询用户列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &sysclient.UserListResp{
		Total: count,
		List:  list,
	}, nil
}
