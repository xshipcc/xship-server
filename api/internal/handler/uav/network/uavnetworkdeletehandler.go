package network

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest/httpx"
	"zero-admin/api/internal/logic/uav/network"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
)

func UavNetworkDeleteHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req types.DeleteUavNetworkReq
		if err := httpx.Parse(r, &req); err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
			return
		}

		l := network.NewUavNetworkDeleteLogic(r.Context(), svcCtx)
		resp, err := l.UavNetworkDelete(&req)
		if err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
		} else {
			httpx.OkJsonCtx(r.Context(), w, resp)
		}
	}
}
