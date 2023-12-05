package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os/exec"
	"strings"
	"time"

	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/internal/config"
	uavdeviceserviceServer "zero-admin/rpc/uav/internal/server/uavdeviceservice"
	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	"github.com/zeromicro/go-zero/core/conf"
	"github.com/zeromicro/go-zero/core/logx"
	"github.com/zeromicro/go-zero/core/service"
	"github.com/zeromicro/go-zero/zrpc"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

var configFile = flag.String("f", "rpc/uav/etc/uav.yaml", "the config file")

func runUavFlight(ip string, port int, rport int, Hangar_ip string, Hangar_port int, Hangar_rport int, cameraip string, cameraport int) {
	execcmd := fmt.Sprintf("python3  drone_projects/client.py %s %d %d  %s %d %d %s %d ", ip, port, rport, Hangar_ip, Hangar_port, Hangar_rport, cameraip, cameraport)

	cmd := exec.Command(execcmd)
	if err := cmd.Start(); err != nil {
		log.Println("exec the aire port cmd ", " failed")
	}
	// // 等待命令执行完
	// cmd.Wait()

}

func main() {
	flag.Parse()

	var c config.Config
	conf.MustLoad(*configFile, &c)
	ctx := svc.NewServiceContext(c)

	//报警指令
	handleAIFunc := func(source []byte) {
		logx.Errorf("AI参数: %s", string(source))
		var alertitem uavmodel.UavMessage
		sctx := context.Background()

		err := json.Unmarshal(source, &alertitem)
		if err != nil {
			fmt.Printf("parse  err:%s\n", err)
		}
		res, err := ctx.UavMMQModel.Insert(sctx, &alertitem)
		if err != nil {
			fmt.Printf("parse  err:%s\n", err)
		} else {
			lastid, _ := res.LastInsertId()
			alertitem.Id = lastid
			data, _ := json.Marshal(alertitem)
			// fmt.Printf("last id %d :%s \n", lastid, data)
			// fmt.Printf("%s", string(data))

			ctx.MMQServer.RawPublish("alert", string(data))

		}

	}

	// handleAlertFunc := func(source []byte) {
	// 	logx.Errorf("Alert 参数: %s", string(source))

	// }
	//飞机起飞控制指令
	handleCtlFunc := func(source []byte) {
		logx.Errorf(": %s", string(source))
		var ctlitem uavlient.UavControlData
		sctx := context.Background()
		err := json.Unmarshal(source, &ctlitem)
		if err != nil {
			fmt.Printf("parse  err:%s\n", err)
		}
		cmp := strings.Compare(ctlitem.Cmd, "fly")
		if cmp == 0 {

			res, err := ctx.UavFlyHistoryModel.Insert(sctx, &uavmodel.UavFlyHistory{
				UavId:      ctlitem.UavId,
				FlyId:      ctlitem.FlyId,
				Operator:   ctlitem.FlyOp,
				CreateTime: time.Now(),
				EndTime:    time.Now(),
			})
			if err != nil {
				fmt.Printf("parse  err:%s\n", err)
			}
			lastid, _ := res.LastInsertId()
			text := fmt.Sprintf("{'cmd':'dofly','data': %d}", lastid)

			ctx.MMQServer.Publish("control", text)

			//start ai process;
		}
		cmp = strings.Compare(ctlitem.Cmd, "fly_over")
		if cmp == 0 {
			sctx := context.Background()
			item, err := ctx.UavFlyHistoryModel.FindOne(sctx, ctlitem.HistoryId)
			if err != nil {
				fmt.Printf("parse  err:%s\n", err)
			}

			item.EndTime = time.Now()

			err = ctx.UavFlyHistoryModel.Update(sctx, item)
			if err != nil {
				fmt.Printf("parse  err:%s\n", err)
			}
			if err != nil {
				fmt.Printf("parse  err:%s\n", err)
			}
		}
		cmp = strings.Compare(ctlitem.Cmd, "corn")
		if cmp == 0 {
			fmt.Printf("load paln corn  .................")

			ctx.CornServer.Stop()
			// count, _ := ctx.UavPlanModel.Count(ctx)
			all, err := ctx.UavPlanModel.FindAll(ctx, 0, 20)
			if err != nil {
				fmt.Printf("load paln error  err:%s\n", err)
			}
			for _, dict := range *all {
				ctx.CornServer.AddFunc(dict.Plan, func() {
					fmt.Println("fly fly.  go go go !")
					text := fmt.Sprintf("{'cmd':'fly','uav_id': %d,'fly_id': %d}", dict.UavId, dict.FlyId)
					ctx.MMQServer.Publish("fly_control/#", text)
				})
				fmt.Printf("load paln error  err:%s\n", dict.Plan)
			}

			ctx.CornServer.Start()
		}
	}

	// count, _ := ctx.UavDeviceModel.Count(ctx)
	// fmt.Printf("uav device is err:%d\n", count)

	// all, err := ctx.UavDeviceModel.FindAll(ctx, 0, 10)
	// fmt.Printf("is err:%s\n", err)
	// itemList := *all
	// if len(itemList) > 0 {
	// 	fmt.Printf("is ssss:%s\n", itemList[0].Ip)
	// 	runUavFlight(itemList[0].Ip, int(itemList[0].Port), int(itemList[0].RPort), itemList[0].HangarIp, int(itemList[0].HangarPort),
	// 		int(itemList[0].HangarRport), itemList[0].CamIp, int(itemList[0].CamPort))
	// }

	// var list []*types.ListUavDeviceData

	// for _, dict := range *all {
	// 	list = append(list, &types.ListUavDeviceData{
	// 		Id:           dict.Id,
	// 		Name:         dict.Name,
	// 		Ip:           dict.Ip,
	// 		Port:         dict.Port,
	// 		R_Port:       dict.RPort,
	// 		Hangar_ip:    dict.HangarIp,
	// 		Hangar_port:  dict.HangarPort,
	// 		Hangar_rport: dict.HangarRport,
	// 		Cam_ip:       dict.CamIp,
	// 		Cam_port:     dict.CamPort,
	// 		Cam_url:      dict.CamUrl,
	// 	})
	// }

	// runUavFlight(c.AIRPORT.IP, c.AIRPORT.PORT, c.AIRPORT.RPORT)

	// handleUavFunc := func(source []byte) {
	// 	logx.Errorf("Uav参数: %s", string(source))
	// 	var alertitem uavmodel.UavFlyHistoryDetail

	// 	err := json.Unmarshal(source, &alertitem)
	// 	if err != nil {
	// 		fmt.Printf("parse  err:%s\n", err)
	// 	}
	// 	_, err = ctx.UavDeviceModel.Insert(context.Background(), &alertitem)
	// 	if err != nil {
	// 		fmt.Printf("parse  err:%s\n", err)
	// 	}
	// }

	s := zrpc.MustNewServer(c.RpcServerConf, func(grpcServer *grpc.Server) {
		uavlient.RegisterUavDeviceServiceServer(grpcServer, uavdeviceserviceServer.NewUavDeviceServiceServer(ctx))

		if c.Mode == service.DevMode || c.Mode == service.TestMode {
			reflection.Register(grpcServer)
		}

	})
	defer s.Stop()

	ctx.MMQServer.Subscription("ai", handleAIFunc)
	// ctx.MMQServer.Subscription("alert/#", handleAlertFunc)
	ctx.MMQServer.Subscription("fly_control/#", handleCtlFunc)
	// text := "{'cmd':'corn'}"
	// ctx.MMQServer.Publish("fly_control", text)

	fmt.Printf("Starting rpc server at %s...\n", c.ListenOn)
	s.Start()
}
