package people

import (
	"net/http"

	"github.com/zeromicro/go-zero/rest/httpx"
	"zero-admin/api/internal/logic/uav/people"
	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"
)

func PeopleUpdateHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		var req types.UpdatePeopleReq
		if err := httpx.Parse(r, &req); err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
			return
		}

		l := people.NewPeopleUpdateLogic(r.Context(), svcCtx)
		resp, err := l.PeopleUpdate(&req)
		if err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
		} else {
			httpx.OkJsonCtx(r.Context(), w, resp)
		}
	}
}
