package camera

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest/httpx"
	"zero-admin/api/internal/logic/uav/camera"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
)

func CamerasAddHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req types.AddCamerasReq
		if err := httpx.Parse(r, &req); err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
			return
		}

		l := camera.NewCamerasAddLogic(r.Context(), svcCtx)
		resp, err := l.CamerasAdd(&req)
		if err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
		} else {
			httpx.OkJsonCtx(r.Context(), w, resp)
		}
	}
}
