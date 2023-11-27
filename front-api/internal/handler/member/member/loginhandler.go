package member

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest/httpx"
	"zero-admin/front-api/internal/logic/member/member"
	"zero-admin/front-api/internal/svc"
	"zero-admin/front-api/internal/types"
)

func LoginHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req types.LoginReq
		if err := httpx.Parse(r, &req); err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
			return
		}

		l := member.NewLoginLogic(r.Context(), svcCtx)
		resp, err := l.Login(&req, httpx.GetRemoteAddr(r))

		if err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
		} else {
			httpx.OkJsonCtx(r.Context(), w, resp)
		}
	}
}
