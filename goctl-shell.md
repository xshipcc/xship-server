1.安装
框架安装 go get -u github.com/zeromicro/go-zero
框架代码生成工具安装 go get -u github.com/zeromicro/go-zero/tools/goctl

2.创建api
进到api/doc/目录执行
goctl api -o admin.api
goctl api go -api admin.api -dir ../

front-pai
front-api/doc
goctl api -o front.api
goctl api go -api front.api -dir ../

3.创建rpc
进到rpc/sys/目录操作
goctl rpc template -o sys.proto
goctl rpc protoc sys.proto --go_out=./ --go-grpc_out=./ --zrpc_out=. -m



进到rpc/mmq/目录操作
goctl rpc protoc mmq.proto --go_out=./ --go-grpc_out=./ --zrpc_out=. -m


进到rpc/uav/目录操作
goctl rpc template -o uav.proto
goctl rpc protoc uav.proto --go_out=./ --go-grpc_out=./ --zrpc_out=. -m

4.创建model
进到rpc/目录操作
goctl model mysql ddl -c -src book.sql -dir .
goctl model mysql datasource -url="root:12345678@tcp(127.0.0.1:3306)/gozero" -table="sys*" -dir ./model/sysmodel

goctl model mysql datasource -url="root:12345678@tcp(127.0.0.1:3306)/gozero" -table="uav*" -dir ./model/uavmodel


5.备份数据库
mysqldump -uroot -p gozero > gozero.db
