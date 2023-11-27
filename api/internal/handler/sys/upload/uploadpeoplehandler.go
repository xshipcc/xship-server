package upload

import (
	"net/http"

	"zero-admin/api/internal/logic/sys/upload"
	"zero-admin/api/internal/svc"

	"github.com/zeromicro/go-zero/rest/httpx"
)

func UploadPeopleHandler(svcCtx *svc.ServiceContext) http.HandlerFunc {
	return func(w http.ResponseWriter, r *http.Request) {
		l := upload.NewUploadPeopleLogic(r, r.Context(), svcCtx)
		resp, err := l.UploadPeople()
		if err != nil {
			httpx.ErrorCtx(r.Context(), w, err)
		} else {
			httpx.OkJsonCtx(r.Context(), w, resp)
		}
	}
}
