package alert

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest/httpx"
	"zero-admin/api/internal/logic/uav/alert"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
)

func AlertItemConfirmHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req types.ConfirmAlertHistoryReq
		if err := httpx.Parse(r, &req); err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
			return
		}

		l := alert.NewAlertItemConfirmLogic(r.Context(), svcCtx)
		resp, err := l.AlertItemConfirm(&req)
		if err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
		} else {
			httpx.OkJsonCtx(r.Context(), w, resp)
		}
	}
}
