package main

import (
	"bytes"
	"context"
	"encoding/json"
	"flag"
	"fmt"
	"log"
	"os"
	"os/exec"
	"strconv"
	"strings"
	"time"

	"zero-admin/rpc/model/uavmodel"
	"zero-admin/rpc/uav/internal/config"
	uavdeviceserviceServer "zero-admin/rpc/uav/internal/server/uavdeviceservice"
	"zero-admin/rpc/uav/internal/svc"
	"zero-admin/rpc/uav/uavlient"

	try_catch "github.com/golang-infrastructure/go-try-catch"
	"github.com/robfig/cron/v3"
	"github.com/zeromicro/go-zero/core/conf"
	"github.com/zeromicro/go-zero/core/logx"
	"github.com/zeromicro/go-zero/core/service"
	"github.com/zeromicro/go-zero/zrpc"
	"google.golang.org/grpc"
	"google.golang.org/grpc/reflection"
)

var configFile = flag.String("f", "rpc/uav/etc/uav.yaml", "the config file")

func runUavFlight(ip string, port int, rport int, Hangar_ip string, Hangar_port int, Hangar_rport int, cameraip string, cameraport int, zubo int, network string, joystick string) *exec.Cmd {

	cmd := exec.Command("python3", "/javodata/drone_projects/client.py", ip, strconv.Itoa(port), strconv.Itoa(rport), cameraip, strconv.Itoa(cameraport), Hangar_ip, strconv.Itoa(Hangar_port), strconv.Itoa(Hangar_rport), strconv.Itoa(zubo), network, joystick)

	fmt.Println("cmd -> ", cmd)

	buf := bytes.Buffer{}
	cmd.Stdout = &buf

	// cmd := exec.Command(execcmd)
	if err := cmd.Start(); err != nil {
		log.Println("exec the  cmd ", " failed")
	}

	fmt.Println("out :" + buf.String())

	return cmd
	// // 等待命令执行完
	// cmd.Wait()

}

// AI
func runAI(camera string, dir string, historyid string) *exec.Cmd {

	cmd := exec.Command("/javodata/deepai", "", camera, dir, historyid, "on", "-w")

	fmt.Println("ai cmd -> ", cmd)
	if err := cmd.Start(); err != nil {
		log.Println("exec the ai cmd ", " failed")
	}
	return cmd
	// // 等待命令执行完
	// cmd.Wait()

}

// // 制造一天的历史数据
// func MakeStatistics(data string, ctx ServiceContext) {

// }

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
		// logx.Errorf("AI参数: %s", string(source))
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
		today := time.Now().Format("2006-01-02")

		data_byte, _ := json.Marshal(alertitem)
		fmt.Printf("str:%v\n", string(data_byte))

		//存储最近50 个点
		var uavpoint uavlient.Uavpoints

		uavpoint.Type = alertitem.Type
		uavpoint.Lon = flon
		uavpoint.Lat = flat
		uavpoint.Alt = falt
		point_byte, _ := json.Marshal(uavpoint)

		ctx.MyRedis.Lpush("points", point_byte)
		lenccount, _ := ctx.MyRedis.Llen("points")
		if lenccount > 50 {
			ctx.MyRedis.Ltrim("points", 0, 1)
		}

		//uav 历史数据
		var uavStatistic uavlient.UavsStatistics

		history, err := ctx.MyRedis.Hget("history", today)
		historyC := []byte(history) // strB len: 8, cap: 8

		if err != nil {
			fmt.Printf("parse  err:%s\n", err)
		} else {
			json.Unmarshal(historyC, &uavStatistic)

		}
		// 0:pedestrian
		// 1: bicycle

		// 2:ca0

		// 3:yan
		// 4: trucK

		// 5: tricycle
		//6: DUS.
		//7: motor
		//8: fire..
		//9: smoke
		//增加数量
		switch alertitem.Type {
		case 0:
			uavStatistic.Person += 1

		case 1:
			uavStatistic.Bicycle += 1

		case 2:
			uavStatistic.Car += 1
		case 3:
			uavStatistic.Bus += 1

		case 4:
			uavStatistic.Truck += 1

		case 5:
			uavStatistic.Tricycle += 1

		case 6:
			uavStatistic.Bus += 1

		case 7:
			uavStatistic.Motorcycle += 1

		case 8:
			uavStatistic.Fire += 1

		case 9:
			uavStatistic.Smoke += 1

		default:

		}
		uavStatistic.Total += 1

		history_byte, _ := json.Marshal(uavStatistic)

		history_string := string(history_byte)
		//存储历史数据
		ctx.MyRedis.Hset("history", today, history_string)

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

			try_catch.Try(func() {
				res, err := ctx.UavFlyHistoryModel.Insert(sctx, &uavmodel.UavFlyHistory{
					UavId:      ctlitem.UavId,
					FlyId:      ctlitem.FlyId,
					Operator:   ctlitem.FlyOp,
					Status:     0,
					Remark:     "",
					CreateTime: time.Now(),
					EndTime:    time.Now(),
					Lat:        ctlitem.Lat,
					Lon:        ctlitem.Lon,
					Alt:        ctlitem.Alt,
				})
				if err != nil {
					fmt.Printf("添加历史  err:%s\n", err)
				}
				fly, err := ctx.UavFlyModel.FindOne(sctx, ctlitem.FlyId)
				if err != nil {
					fmt.Printf("查找飞行路线  err:%s\n", err)
				}
				lastid, _ := res.LastInsertId()
				var flydata uavlient.UavFlyData
				flydata.Cmd = "dofly"
				flydata.Data = fly.Data
				flydata.Historyid = lastid

				flysend, err := json.Marshal(flydata)

				oneuav, err := ctx.UavDeviceModel.FindOneActive(sctx)
				if err != nil {
					fmt.Printf("当前飞机数据  err:%s\n", err)
				}
				if ctx.AICmd != nil {
					ctx.AICmd.Process.Kill()
				}
				fmt.Printf("启动巡航  :%d\n", lastid)

				slast := strconv.FormatInt(lastid, 10)
				folderPath := "uploads"

				if _, err := os.Stat(folderPath); os.IsNotExist(err) {
					// 必须分成两步：先创建文件夹、再修改权限
					os.Mkdir(folderPath, 0777) //0777也可以os.ModePerm
				}

				ctx.AICmd = runAI(oneuav.CamUrl, folderPath, slast)

				ctx.MMQServer.Publish("control", flysend)
			}).DefaultCatch(func(err error) {
				fmt.Println("---->catch", err)
			}).Finally(func() {
				fmt.Println("---->finally")
			}).Do()
			//start ai process;
		}
		cmp = strings.Compare(ctlitem.Cmd, "fly_over")
		if cmp == 0 {
			sctx := context.Background()
			try_catch.Try(func() {

				item, err := ctx.UavFlyHistoryModel.FindOne(sctx, ctlitem.HistoryId)
				if err != nil {
					fmt.Printf("parse  err:%s\n", err)
				}

				item.EndTime = time.Now()
				item.Status = ctlitem.FlyId
				item.Remark = ctlitem.Data

				err = ctx.UavFlyHistoryModel.Update(sctx, item)
				if err != nil {
					fmt.Printf("parse  err:%s\n", err)
				}
				if err != nil {
					fmt.Printf("parse  err:%s\n", err)
				}

				var flyover uavlient.UavFlyData
				flyover.Cmd = "fly_over"
				flysend, err := json.Marshal(flyover)
				ctx.MMQServer.Publish("control", flysend)

				if ctx.AICmd != nil {
					ctx.AICmd.Process.Kill()
				}
			}).DefaultCatch(func(err error) {
				fmt.Println("---->catch", err)
			}).Finally(func() {
				fmt.Println("---->finally")
			}).Do()
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

			try_catch.Try(func() {
				sctx := context.Background()
				// count, _ := ctx.UavDeviceModel.Count(sctx)
				// fmt.Printf("is count: %d\n", count)
				if ctx.Cmd != nil {
					ctx.Cmd.Process.Kill()
				}
				oneuav, err := ctx.UavDeviceModel.FindOneActive(sctx)
				fmt.Printf("-------startuav---------> err:%x %s\n", oneuav, err)
				if oneuav != nil {
					ctx.Cmd = runUavFlight(oneuav.Ip, int(oneuav.Port), int(oneuav.RPort), oneuav.HangarIp, int(oneuav.HangarPort),
						int(oneuav.HangarRport), oneuav.CamIp, int(oneuav.CamPort), int(oneuav.UavZubo), oneuav.Network, oneuav.Joystick)
				}
			}).DefaultCatch(func(err error) {
				fmt.Println("---->catch", err)
			}).Finally(func() {
				fmt.Println("---->finally")
			}).Do()

		}
		cmp = strings.Compare(ctlitem.Cmd, "corn")
		if cmp == 0 {
			try_catch.Try(func() {

				if ctx.CornServer != nil {
					ctx.CornServer.Stop()
				}
				ctx.CornServer = cron.New(cron.WithSeconds())
				// count, _ := ctx.UavPlanModel.Count(ctx)
				all, err := ctx.UavPlanModel.FindAll(ctx, 1, 1)
				if err != nil {
					fmt.Printf("load paln error  err:%s\n", err)
				}
				for _, dict := range *all {

					ctx.CornServer.AddFunc(dict.Plan, func() {
						fmt.Println("fly fly.  go go go !")
						var sendctl uavlient.UavControlData
						sendctl.Cmd = "fly"
						sendctl.UavId = dict.UavId
						sendctl.FlyId = dict.FlyId
						flysend, _ := json.Marshal(sendctl)

						ctx.MMQServer.Publish("fly_control", flysend)

					})
					fmt.Printf("load paln :%s\n", dict.Plan)
				}

				ctx.CornServer.Start()
			}).DefaultCatch(func(err error) {
				fmt.Println("---->catch", err)
			}).Finally(func() {
				fmt.Println("---->finally")
			}).Do()
		}
	}

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
	ctx.StaticCornServer = cron.New(cron.WithSeconds())
	// Generate daily statistics for the previous day.
	// Gets yesterday's statistics from Redis, creates snapshot data,
	// inserts into database.
	ctx.StaticCornServer.AddFunc("0 0 1 * * ?", func() {
		fmt.Println("Gen Yestday Statistics !")
		now := time.Now()
		year, month, day := now.Date()

		// 今日日期
		today := time.Date(year, month, day, 0, 0, 0, 0, time.Local)
		fmt.Println("今日日期:", today)

		// 昨日日期
		yesterday := today.AddDate(0, 0, -1)
		fmt.Println("昨日日期:", yesterday)
		sctx := context.Background()

		fmt.Printf("MakeStatistics---->  data:%s\n", yesterday)
		var uavStatistic uavlient.UavsStatistics

		history, err := ctx.MyRedis.Hget("history", yesterday.Format("2006-01-02"))
		historyC := []byte(history) // strB len: 8, cap: 8

		if err != nil {
			fmt.Printf("parse  err:%s\n", err)
		} else {
			json.Unmarshal(historyC, &uavStatistic)

		}

		//get Snapshot

		person := []string{}
		all, _ := ctx.UavMMQModel.FindCount(sctx, 0, 5)
		for _, dict := range *all {
			person = append(person, dict.Image)
		}
		car := []string{}
		all, _ = ctx.UavMMQModel.FindCount(sctx, 1, 5)
		for _, dict := range *all {
			car = append(car, dict.Image)
		}
		truck := []string{}
		all, _ = ctx.UavMMQModel.FindCount(sctx, 2, 5)
		for _, dict := range *all {
			truck = append(truck, dict.Image)
		}
		motorcycle := []string{}
		all, _ = ctx.UavMMQModel.FindCount(sctx, 3, 5)
		for _, dict := range *all {
			motorcycle = append(motorcycle, dict.Image)
		}
		bicycle := []string{}
		all, _ = ctx.UavMMQModel.FindCount(sctx, 4, 5)
		for _, dict := range *all {
			bicycle = append(bicycle, dict.Image)
		}
		bus := []string{}
		all, _ = ctx.UavMMQModel.FindCount(sctx, 5, 5)
		for _, dict := range *all {
			bus = append(bus, dict.Image)
		}
		boxtruck := []string{}
		all, _ = ctx.UavMMQModel.FindCount(sctx, 6, 5)
		for _, dict := range *all {
			boxtruck = append(boxtruck, dict.Image)
		}
		tricycle := []string{}
		all, _ = ctx.UavMMQModel.FindCount(sctx, 7, 5)
		for _, dict := range *all {
			tricycle = append(tricycle, dict.Image)
		}
		smoke := []string{}
		all, _ = ctx.UavMMQModel.FindCount(sctx, 8, 5)
		for _, dict := range *all {
			smoke = append(smoke, dict.Image)
		}
		fire := []string{}
		all, _ = ctx.UavMMQModel.FindCount(sctx, 9, 5)
		for _, dict := range *all {
			fire = append(fire, dict.Image)
		}

		// var jsonSlice []map[string]interface{}
		mjson := map[string]interface{}{
			"person":     person,
			"car":        car,
			"truck":      truck,
			"motorcycle": motorcycle,
			"bicycle":    bicycle,
			"bus":        bus,
			"boxtruck":   boxtruck,
			"tricycle":   tricycle,
			"smoke":      smoke,
			"fire":       fire,
		}

		snapshots, _ := json.Marshal(mjson)

		try_catch.Try(func() {
			_, err := ctx.UavStatModel.Insert(sctx, &uavmodel.UavStatistics{
				Total:      uavStatistic.Total,
				Person:     uavStatistic.Person,
				Car:        uavStatistic.Car,
				Truck:      uavStatistic.Truck,
				Motorcycle: uavStatistic.Motorcycle,
				Bicycle:    uavStatistic.Bicycle,
				Bus:        uavStatistic.Bus,
				BoxTruck:   uavStatistic.BoxTruck,
				Tricycle:   uavStatistic.Tricycle,
				Smoke:      uavStatistic.Smoke,
				Fire:       uavStatistic.Fire,
				Remark:     "",
				Snapshots:  string(snapshots),
				CreateTime: yesterday,
			})
			if err != nil {
				fmt.Printf("添加历史  err:%s\n", err)
			}

			// slast := strconv.FormatInt(lastid, 10)
			// ctx.AICmd = runAI(oneuav.CamUrl, "/javodata/history", slast)

		}).DefaultCatch(func(err error) {
			fmt.Println("---->catch", err)
		}).Finally(func() {
			fmt.Println("---->finally")
		}).Do()
	})

	time.Sleep(2 * time.Second)

	var flydata uavlient.UavFlyData
	flydata.Cmd = "start_uav"

	flysend, _ := json.Marshal(flydata)
	ctx.MMQServer.Publish("fly_control", flysend)

	flydata.Cmd = "corn"

	flysend, _ = json.Marshal(flydata)
	ctx.MMQServer.Publish("fly_control", flysend)

	fmt.Printf("Starting uav rpc server at %s...\n", c.ListenOn)
	s.Start()
}
