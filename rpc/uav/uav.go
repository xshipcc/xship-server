package main

import (
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os/exec"
	"strconv"
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

func runUavFlight(ip string, port int, rport int, Hangar_ip string, Hangar_port int, Hangar_rport int, cameraip string, cameraport int, url string) {
	//execcmd := fmt.Sprintf("python3  drone_projects/client.py %s %d %d  %s %d %s %d %d ", ip, port, rport, cameraip, cameraport, Hangar_ip, Hangar_port, Hangar_rport)

	cmd := exec.Command("python3", "drone_projects/client.py", ip, strconv.Itoa(port), strconv.Itoa(rport), cameraip, strconv.Itoa(cameraport), Hangar_ip, strconv.Itoa(Hangar_port), strconv.Itoa(Hangar_rport), url)

	fmt.Println("cmd -> ", cmd)
	// cmd := exec.Command(execcmd)
	if err := cmd.Start(); err != nil {
		log.Println("exec the aire port cmd ", " failed")
	}
	// // 等待命令执行完
	// cmd.Wait()

}

func Itoa(port int) {
	panic("unimplemented")
}

func MakeAFly(port int) {
	panic("unimplemented")
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
		fmt.Printf("str:%s\n", alertitem.Image)

		lon, _ := ctx.MyRedis.Get("lon")
		lat, _ := ctx.MyRedis.Get("lat")
		alt, _ := ctx.MyRedis.Get("height")
		// b, err = ctx.Redis.Float64(ctx.Redis.Do("ZINCRBY", "z", 2.5, "member"))
		flon, _ := strconv.ParseFloat(lon, 64)
		flat, _ := strconv.ParseFloat(lat, 64)
		falt, _ := strconv.ParseFloat(alt, 64)

		alertitem.Lon = flon
		alertitem.Lat = flat
		alertitem.Alt = falt
		// alertitem.StartTime = time.Now().Format("2006-01-02 15:04:05")

		data_byte, _ := json.Marshal(alertitem)
		fmt.Printf("str:%v\n", string(data_byte))

		// alertitem.Lon
		res, err := ctx.UavMMQModel.Insert(sctx, &alertitem)
		if err != nil {
			fmt.Printf("parse  err:%s\n", err)
		} else {
			lastid, _ := res.LastInsertId()
			alertitem.Id = lastid
			var alert uavlient.UavAlertData
			alert.Image = alertitem.Image
			alert.Type = alertitem.Type
			alert.Lon = flon
			alert.Lat = flat
			alert.Alt = falt
			data, _ := json.Marshal(alert)
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
				fmt.Printf("添加历史  err:%s\n", err)
			}
			fly, err := ctx.UavFlyModel.FindOne(sctx, ctlitem.FlyId)
			if err != nil {
				fmt.Printf("航线  err:%s\n", err)
			}
			lastid, _ := res.LastInsertId()
			var flydata uavlient.UavFlyData
			flydata.Cmd = "dofly"
			flydata.Data = fly.Data
			flydata.Historyid = lastid

			flysend, err := json.Marshal(flydata)
			// text := fmt.Sprintf('{"cmd":"dofly","data":%s ,"historyid": %d}', flydata, lastid)

			ctx.MMQServer.Publish("control", flysend)

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

		// cmp = strings.Compare(ctlitem.Cmd, "autofly")
		// if cmp == 0 {
		// 	plan, err := ctx.UavPlanModel.FindOne(sctx, ctlitem.FlyId)
		// 	if err != nil {
		// 		fmt.Printf("航线  err:%s\n", err)
		// 		return
		// 	}
		// 	res, err := ctx.UavFlyHistoryModel.Insert(sctx, &uavmodel.UavFlyHistory{
		// 		UavId:      plan.UavId,
		// 		FlyId:      plan.FlyId,
		// 		Operator:   ctlitem.FlyOp,
		// 		CreateTime: time.Now(),
		// 		EndTime:    time.Now(),
		// 	})
		// 	if err != nil {
		// 		fmt.Printf("添加历史  err:%s\n", err)
		// 	}
		// 	fly, err := ctx.UavFlyModel.FindOne(sctx, ctlitem.FlyId)
		// 	if err != nil {
		// 		fmt.Printf("航线  err:%s\n", err)
		// 	}
		// 	lastid, _ := res.LastInsertId()
		// 	var flydata uavlient.UavFlyData
		// 	flydata.Cmd = "dofly"
		// 	flydata.Data = fly.Data
		// 	flydata.Historyid = lastid

		// 	flysend, err := json.Marshal(flydata)

		// 	ctx.MMQServer.Publish("control", flysend)

		// 	//start ai process;
		// }
		cmp = strings.Compare(ctlitem.Cmd, "start_uav")
		if cmp == 0 {
			sctx := context.Background()
			// count, _ := ctx.UavDeviceModel.Count(sctx)
			// fmt.Printf("is count: %d\n", count)
			all, err := ctx.UavDeviceModel.FindAll(sctx, 1, 10)
			fmt.Printf("----------------> err:%s\n", err)
			itemList := *all
			if len(itemList) > 0 {
				// fmt.Printf("start :%s\n", itemList[0].Ip)
				runUavFlight(itemList[0].Ip, int(itemList[0].Port), int(itemList[0].RPort), itemList[0].HangarIp, int(itemList[0].HangarPort),
					int(itemList[0].HangarRport), itemList[0].CamIp, int(itemList[0].CamPort), itemList[0].CamUrl)
			}
		}
		cmp = strings.Compare(ctlitem.Cmd, "corn")
		if cmp == 0 {
			fmt.Printf("load paln corn  .................")

			ctx.CornServer.Stop()
			// count, _ := ctx.UavPlanModel.Count(ctx)
			all, err := ctx.UavPlanModel.FindAll(ctx, 1, 1)
			if err != nil {
				fmt.Printf("load paln error  err:%s\n", err)
			}
			for _, dict := range *all {

				ctx.CornServer.AddFunc(dict.Plan, func() {
					fmt.Println("fly fly.  go go go !")
					text := fmt.Sprintf("{'cmd':'fly','uav_id': %d,'fly_id': %d}", dict.UavId, dict.FlyId)
					ctx.MMQServer.Publish("control", text)

				})
				fmt.Printf("load paln :%s\n", dict.Plan)
			}

			ctx.CornServer.Start()
		}
	}

	// count, _ := ctx.UavDeviceModel.Count(ctx)
	// fmt.Printf("uav device is err:%d\n", count)
	// sctx := context.Background()
	// all, err := ctx.UavDeviceModel.FindAll(sctx, 0, 10)
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
	ctx.MMQServer.Publish("fly_control", "start_uav")

	fmt.Printf("Starting rpc server at %s...\n", c.ListenOn)
	s.Start()
}
