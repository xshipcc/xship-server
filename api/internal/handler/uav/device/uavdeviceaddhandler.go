package device

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest/httpx"
	"zero-admin/api/internal/logic/uav/device"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
)

func UavDeviceAddHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req types.AddUavDeviceReq
		if err := httpx.Parse(r, &req); err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
			return
		}

		l := device.NewUavDeviceAddLogic(r.Context(), svcCtx)
		resp, err := l.UavDeviceAdd(&req)
		if err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
		} else {
			httpx.OkJsonCtx(r.Context(), w, resp)
		}
	}
}
