package upload

import (
	"context"
	"fmt"
	"io"
	"net/http"
	"os"
	"path/filepath"

	"zero-admin/api/internal/svc"
	"zero-admin/api/internal/types"

	"github.com/zeromicro/go-zero/core/logx"
)

type UploadCarLogic struct {
	logx.Logger
	ctx    context.Context
	svcCtx *svc.ServiceContext
	r      *http.Request
}

func NewUploadCarLogic(r *http.Request, ctx context.Context, svcCtx *svc.ServiceContext) *UploadCarLogic {
	return &UploadCarLogic{
		Logger: logx.WithContext(ctx),
		ctx:    ctx,
		svcCtx: svcCtx,
		r:      r,
	}
}

func (l *UploadCarLogic) UploadCar() (resp *types.UploadResp, err error) {
	file, handler, err := l.r.FormFile("file")
	logx.WithContext(l.ctx).Infof("File uploaded successfully: %s", handler.Filename)
	if err != nil {
		logx.WithContext(l.ctx).Errorf("Error retrieving the file,异常:%s", err.Error())
		return nil, err
	}
	defer file.Close()

	err = os.MkdirAll("./uploads/car/", os.ModePerm)
	if err != nil {
		logx.WithContext(l.ctx).Errorf("Failed to create directory,异常:%s", err.Error())
		return nil, err
	}
	// 创建一个新的文件来保存上传的文件
	uploadedFile, err := os.Create(filepath.Join("./uploads/car/", handler.Filename))
	if err != nil {
		logx.WithContext(l.ctx).Errorf("Error creating the filee,异常:%s", err.Error())
		return nil, err
	}
	defer uploadedFile.Close()

	// 将上传的文件拷贝到新文件中
	_, err = io.Copy(uploadedFile, file)
	if err != nil {
		logx.WithContext(l.ctx).Errorf("Error copying the file,异常:%s", err.Error())
		return nil, err
	}

	path := fmt.Sprintf("/uploads/car/%s", handler.Filename)

	logx.WithContext(l.ctx).Infof("File uploaded successfully: %s", handler.Filename)
	return &types.UploadResp{
		Code:    "000000",
		Message: "上传文件成功",
		Data:    path,
	}, nil
}
