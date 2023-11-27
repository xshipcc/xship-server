package device

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest/httpx"
	"zero-admin/api/internal/logic/uav/device"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
)

func UavDeviceDeleteHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req types.DeleteUavDeviceReq
		if err := httpx.Parse(r, &req); err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
			return
		}

		l := device.NewUavDeviceDeleteLogic(r.Context(), svcCtx)
		resp, err := l.UavDeviceDelete(&req)
		if err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
		} else {
			httpx.OkJsonCtx(r.Context(), w, resp)
		}
	}
}
