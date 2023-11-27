package albumpicservicelogic

import (
	"context"
	"encoding/json"
	"zero-admin/rpc/pms/internal/svc"
	"zero-admin/rpc/pms/pmsclient"

	"github.com/zeromicro/go-zero/core/logx"
)

type AlbumPicListLogic struct {
	ctx    context.Context
	svcCtx *svc.ServiceContext
	logx.Logger
}

func NewAlbumPicListLogic(ctx context.Context, svcCtx *svc.ServiceContext) *AlbumPicListLogic {
	return &AlbumPicListLogic{
		ctx:    ctx,
		svcCtx: svcCtx,
		Logger: logx.WithContext(ctx),
	}
}

func (l *AlbumPicListLogic) AlbumPicList(in *pmsclient.AlbumPicListReq) (*pmsclient.AlbumPicListResp, error) {
	all, err := l.svcCtx.PmsAlbumPicModel.FindAll(l.ctx, in.Current, in.PageSize)
	count, _ := l.svcCtx.PmsAlbumPicModel.Count(l.ctx)

	if err != nil {
		reqStr, _ := json.Marshal(in)
		logx.WithContext(l.ctx).Errorf("查询相册图片列表信息失败,参数:%s,异常:%s", reqStr, err.Error())
		return nil, err
	}

	var list []*pmsclient.AlbumPicListData
	for _, item := range *all {

		list = append(list, &pmsclient.AlbumPicListData{
			Id:      item.Id,
			AlbumId: item.AlbumId,
			Pic:     item.Pic,
		})
	}

	reqStr, _ := json.Marshal(in)
	listStr, _ := json.Marshal(list)
	logx.WithContext(l.ctx).Infof("查询相册图片列表信息,参数：%s,响应：%s", reqStr, listStr)
	return &pmsclient.AlbumPicListResp{
		Total: count,
		List:  list,
	}, nil
}
