package main

import (
	// "bytes"
	"bufio"
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

func runUavFlight(id int, ip string, port int, rport int, Hangar_ip string, Hangar_port int, Hangar_rport int, cameraip string, cameraport int, zubo int, network string, joystick string) *exec.Cmd {

	cmd := exec.Command("python3", "/javodata/drone_projects/client.py", strconv.Itoa(id), ip, strconv.Itoa(port), strconv.Itoa(rport), cameraip, strconv.Itoa(cameraport), Hangar_ip, strconv.Itoa(Hangar_port), strconv.Itoa(Hangar_rport), strconv.Itoa(zubo), network, joystick)

	fmt.Println("start uav cmd -> ", cmd)

	cmd.Dir = "/javodata"
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		log.Println("exec the  cmd ", " failed")
	}
	if err := cmd.Start(); err != nil {
		log.Println("exec the  Start ", " failed")
	}

	go func() {

		try_catch.Try(func() {

			scanner := bufio.NewScanner(stdout)
			for scanner.Scan() {
				fmt.Println(scanner.Text())
			}
			if err := scanner.Err(); err != nil {
				// panic(err)
				fmt.Println("---cmd ->read", err)

			}
			if err := cmd.Wait(); err != nil {
				// panic(err)
			}

		}).DefaultCatch(func(err error) {
			fmt.Println("---cmd->catch", err)
		}).Finally(func() {
			fmt.Println("--cmd-->finally")
		}).Do()

	}()
	return cmd

}

// AI
func runAI(ctx *svc.ServiceContext, camera string, dir string, historyid string, ai_id string, show string, save string) *exec.Cmd {

	cmd := exec.Command("/javodata/deepai", camera, dir, historyid, ai_id, show, save)

	fmt.Println("ai cmd -> ", cmd)

	cmd.Dir = "/javodata"
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		log.Println("exec ai  cmd ", " failed")
	}
	if err := cmd.Start(); err != nil {
		log.Println("exec ai  Start ", " failed")
	}

	go func() {

		try_catch.Try(func() {

			scanner := bufio.NewScanner(stdout)
			for scanner.Scan() {
				fmt.Println(scanner.Text())
			}
			if err := scanner.Err(); err != nil {
				fmt.Println("---cmd ai->read", err)
				// panic(err)
			}
			if err := cmd.Wait(); err != nil {
				// panic(err)
			}
			ctx.AICmd = nil

		}).DefaultCatch(func(err error) {
			fmt.Println("---cmd ai->catch", err)
			ctx.AICmd = nil
		}).Finally(func() {
			fmt.Println("--cmd ai-->finally")
			ctx.AICmd = nil
		}).Do()

	}()
	return cmd
	// // 等待命令执行完
	// cmd.Wait()

}

// runFFMPEG
func runFFMPEG(input_file string, out_file string) *exec.Cmd {

	cmd := exec.Command("/usr/local/bin/ffmpeg", "-re", "-i", "/javodata/"+input_file, "-vcodec", "h264", "-acodec", "aac", "-strict", "-2", "/javodata/"+out_file)

	fmt.Println("ffmpeg cmd -> ", cmd)

	cmd.Dir = "/javodata"
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		log.Println("exec ffmpeg  cmd ", " failed")
	}
	if err := cmd.Start(); err != nil {
		log.Println("exec ffmpeg  Start ", " failed")
	}

	go func() {

		try_catch.Try(func() {

			scanner := bufio.NewScanner(stdout)
			for scanner.Scan() {
				fmt.Println(scanner.Text())
			}
			if err := scanner.Err(); err != nil {
				fmt.Println("---cmd ffmpeg->read", err)
				// panic(err)
			}
			if err := cmd.Wait(); err != nil {
				// panic(err)
			}

		}).DefaultCatch(func(err error) {
			fmt.Println("---cmd ffmpeg->catch", err)
		}).Finally(func() {
			fmt.Println("--cmd ffmpeg-->finally")
		}).Do()

	}()
	return cmd
	// // 等待命令执行完
	// cmd.Wait()

}

// runFFMPEG
func PlayFile(file string) *exec.Cmd {

	cmd := exec.Command("totem", file)

	fmt.Println("PlayFile cmd -> ", cmd)

	cmd.Dir = "/javodata"
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		log.Println("exec PlayFile  cmd ", " failed")
	}
	if err := cmd.Start(); err != nil {
		log.Println("exec PlayFile  Start ", " failed")
	}

	go func() {

		try_catch.Try(func() {

			scanner := bufio.NewScanner(stdout)
			for scanner.Scan() {
				fmt.Println(scanner.Text())
			}
			if err := scanner.Err(); err != nil {
				fmt.Println("---cmd PlayFile->read", err)
				// panic(err)
			}
			if err := cmd.Wait(); err != nil {
				// panic(err)
			}

		}).DefaultCatch(func(err error) {
			fmt.Println("---cmd PlayFile->catch", err)
		}).Finally(func() {
			fmt.Println("--cmd PlayFile-->finally")
		}).Do()

	}()
	return cmd
	// // 等待命令执行完
	// cmd.Wait()

}

// // 制造一天的历史数据
// func MakeStatistics(data string, ctx ServiceContext) {

// }

func main() {
	flag.Parse()

	var c config.Config
	conf.MustLoad(*configFile, &c)
	ctx := svc.NewServiceContext(c)

	//报警指令
	handleAIFunc := func(source []byte) {
		var ctlitem uavlient.UavControlData
		err := json.Unmarshal(source, &ctlitem)
		var alertitem uavmodel.UavMessage
		err = json.Unmarshal(source, &alertitem)
		sctx := context.Background()
		if err != nil {
			fmt.Printf("parse  err:%s\n", err)
		}
		// fmt.Printf("str:%s\n", alertitem.Image)
		//无人机数据更新
		if alertitem.Platform == 1 {
			uav_id, _ := ctx.MyRedis.Get("uav")

			lon, _ := ctx.MyRedis.Hget(uav_id, "lon")
			lat, _ := ctx.MyRedis.Hget(uav_id, "lat")
			alt, _ := ctx.MyRedis.Hget(uav_id, "height")
			// b, err = ctx.Redis.Float64(ctx.Redis.Do("ZINCRBY", "z", 2.5, "member"))
			flon, _ := strconv.ParseFloat(lon, 64)
			flat, _ := strconv.ParseFloat(lat, 64)
			falt, _ := strconv.ParseFloat(alt, 64)
			fmt.Printf("str:%f %f %f \n", flon, flat, falt)

			alertitem.Lon = flon
			alertitem.Lat = flat
			alertitem.Alt = falt
			alertitem.HistoryId = ctlitem.HistoryId
		} else if alertitem.Platform == 2 {

			onecam, err := ctx.UavCameraModel.FindOne(sctx, ctlitem.HistoryId)
			if err != nil {
				fmt.Printf("find camera  err:%s\n", err)
				return
			}
			fmt.Printf("find camera :%f\n", onecam.Name)

			//2 ai. HistoryId 就是 摄像头id
			alertitem.Lon = onecam.Lon
			alertitem.Lat = onecam.Lat
			alertitem.Alt = onecam.Alt
			alertitem.HistoryId = ctlitem.HistoryId
		}

		alertitem.CreateTime = time.Now()
		today := time.Now().Format("2006-01-02")

		// data_byte, _ := json.Marshal(alertitem)
		// fmt.Printf("str:%v\n", string(data_byte))

		//存储最近50 个点
		var uavpoint uavlient.Uavpoints

		uavpoint.Type = alertitem.Type
		uavpoint.Lon = alertitem.Lon
		uavpoint.Lat = alertitem.Lat
		uavpoint.Alt = alertitem.Alt
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
			uavStatistic.Car += 1

		case 2:
			uavStatistic.Bicycle += 1

		case 3:
			uavStatistic.Bus += 1

		case 4:
			uavStatistic.Truck += 1

		case 5:
			uavStatistic.BoxTruck += 1

		case 6:
			uavStatistic.Tricycle += 1

		case 7:
			uavStatistic.Motorcycle += 1

		case 8:
			uavStatistic.Smoke += 1

		case 9:
			uavStatistic.Fire += 1

		default:

		}
		uavStatistic.Total += 1

		history_byte, _ := json.Marshal(uavStatistic)

		history_string := string(history_byte)
		//存储历史数据
		ctx.MyRedis.Hset("history", today, history_string)

		if len(alertitem.Image) > 0 {
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
				alert.Lon = alertitem.Lon
				alert.Lat = alertitem.Lat
				alert.Alt = alertitem.Alt
				alert.StartTime = alertitem.CreateTime.Format("2006-01-02")
				data, _ := json.Marshal(alert)
				// fmt.Printf("last id %d :%s \n", lastid, data)
				fmt.Printf("%s", string(data))

				ctx.MMQServer.RawPublish("alert", string(data))

			}
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

				oneuav, err := ctx.UavDeviceModel.FindOne(sctx, ctlitem.UavId)
				if err != nil {
					fmt.Printf("当前飞机数据  err:%s\n", err)
					return
				}
				if oneuav.Status == 1 {

					fly, err := ctx.UavFlyModel.FindOne(sctx, ctlitem.FlyId)
					if err != nil {
						fmt.Printf("查找飞行路线  err:%s\n", err)
						return
					}
					today := time.Now().Format("2006-01-02")
					fmt.Printf("->>查找飞机和航线信息  %s : %s ", oneuav.Name, fly.Name)

					uav_id, _ := ctx.MyRedis.Get("uav")

					lon, _ := ctx.MyRedis.Hget(uav_id, "lon")
					lat, _ := ctx.MyRedis.Hget(uav_id, "lat")
					alt, _ := ctx.MyRedis.Hget(uav_id, "height")
					// b, err = ctx.Redis.Float64(ctx.Redis.Do("ZINCRBY", "z", 2.5, "member"))
					flon, _ := strconv.ParseFloat(lon, 64)
					flat, _ := strconv.ParseFloat(lat, 64)
					falt, _ := strconv.ParseFloat(alt, 64)

					uavhistory := uavmodel.UavFlyHistory{
						UavId:      ctlitem.UavId,
						UavName:    oneuav.Name,
						FlyId:      ctlitem.FlyId,
						RoadName:   fly.Name,
						Operator:   ctlitem.FlyOp,
						Status:     0,
						Remark:     "",
						Path:       "",
						FlyData:    fly.Data,
						CreateTime: time.Now(),
						EndTime:    time.Now(),
						Lat:        flat,
						Lon:        flon,
						Alt:        falt,
					}
					//Gen Fly success
					res, err := ctx.UavFlyHistoryModel.Insert(sctx, &uavhistory)
					if err != nil {
						fmt.Printf("添加历史  err:%s\n", err)
						return
					}

					lastid, _ := res.LastInsertId()
					fmt.Printf("添加历史 %d\n", lastid)

					var flydata uavlient.UavFlyData
					flydata.Cmd = "dofly"
					flydata.Data = fly.Data
					flydata.Historyid = lastid

					flysend, err := json.Marshal(flydata)
					if err != nil {
						fmt.Printf("flysend  err:%s\n", err)
						return
					}

					// if ctx.AICmd != nil {
					// 	ctx.AICmd.Process.Kill()
					// }
					fmt.Printf("启动巡航  :%d\n", lastid)

					slast := strconv.FormatInt(lastid, 10)

					folderPath := "uploads/" + today + "/" + slast

					item, err := ctx.UavFlyHistoryModel.FindOne(sctx, lastid)
					if err != nil {
						fmt.Printf("fubd  err:%s\n", err)
						return
					}

					item.Path = folderPath
					ctx.UavFlyHistoryModel.Update(sctx, item)

					if _, err := os.Stat(folderPath); os.IsNotExist(err) {
						// 必须分成两步：先创建文件夹、再修改权限
						os.MkdirAll(folderPath, 0777) //0777也可以os.ModePerm
					}

					ctx.AICmd = runAI(ctx, oneuav.CamUrl, folderPath, slast, "-1", "on", "save")

					ctx.MMQServer.Publish("control", flysend)
				}
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
				// conver to mp4
				runFFMPEG(item.Path+"/record.avi", item.Path+"/record.mp4")

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
				// fmt.Printf("-------startuav---------> err:%x %s\n", oneuav, err)
				if err == nil {

					ctx.Cmd = runUavFlight(int(oneuav.Id), oneuav.Ip, int(oneuav.Port), int(oneuav.RPort), oneuav.HangarIp, int(oneuav.HangarPort),
						int(oneuav.HangarRport), oneuav.CamIp, int(oneuav.CamPort), int(oneuav.UavZubo), oneuav.Network, oneuav.Joystick)

				}

			}).DefaultCatch(func(err error) {
				fmt.Println("---->catch", err)
			}).Finally(func() {
				fmt.Println("---->finally")
			}).Do()

		}
		cmp = strings.Compare(ctlitem.Cmd, "start_ai")
		if cmp == 0 {

			try_catch.Try(func() {
				sctx := context.Background()

				for _, dict := range ctx.CamAICmd {
					if dict != nil {
						dict.Process.Kill()
					}
				}

				allai, err := ctx.UavCameraModel.FindAllActived(sctx, 1, 10)
				if err == nil {
					today := time.Now().Format("2006-01-02")

					for _, dict := range *allai {

						folderPath := "uploads/ai/" + today + "/" + strconv.Itoa(int(dict.Tunnel))
						if _, err := os.Stat(folderPath); os.IsNotExist(err) {
							// 必须分成两步：先创建文件夹、再修改权限
							os.MkdirAll(folderPath, 0777) //0777也可以os.ModePerm
						}

						letcam := runAI(ctx, dict.RtspUrl, folderPath, "-1", strconv.Itoa(int(dict.Id)), "off", "unsave")
						ctx.CamAICmd = append(ctx.CamAICmd, letcam)

						fmt.Printf("load ai %d success :\n", dict.Tunnel)
					}

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
				all, err := ctx.UavPlanModel.FindAll(ctx, "", "", 1, 20)
				if err != nil {
					fmt.Printf("load paln error  err:%s\n", err)
				}
				for _, dict := range *all {

					if dict.Status == 1 {
						ctx.CornServer.AddFunc(dict.Plan, func() {
							fmt.Println("fly fly.  go go go !")

							uav_id, _ := ctx.MyRedis.Get("uav")
							plan, _ := ctx.MyRedis.Hget(uav_id, "plan")
							p, _ := strconv.ParseInt(plan, 10, 64)
							fmt.Printf("do plan :%d   = %d\n", p, dict.Id)
							if p == dict.Id {
								var sendctl uavlient.UavControlData
								sendctl.Cmd = "fly"
								sendctl.UavId = dict.UavId
								sendctl.FlyId = dict.FlyId
								flysend, _ := json.Marshal(sendctl)

								ctx.MMQServer.Publish("fly_control", flysend)
							}

						})
					}
					fmt.Printf("load paln :%s\n", dict.Plan)
				}

				ctx.CornServer.Start()
			}).DefaultCatch(func(err error) {
				fmt.Println("---->catch", err)
			}).Finally(func() {
				fmt.Println("---->finally")
			}).Do()
		}

		//replay
		cmp = strings.Compare(ctlitem.Cmd, "player/play")
		if cmp == 0 {

			item, err := ctx.UavFlyHistoryModel.FindOne(sctx, ctlitem.HistoryId)
			if err != nil {
				fmt.Printf("parse  err:%s\n", err)
			}
			fmt.Println("---->item.Path  %s", item.Path)

			var sendctl uavlient.UavControlData
			sendctl.Cmd = "replay"
			sendctl.Data = item.Path + "/record.mp4"

			if ctx.PlayerCmd != nil {
				ctx.PlayerCmd.Process.Kill()
			}
			ctx.PlayerCmd = PlayFile(item.Path + "/record.avi")

			flysend, _ := json.Marshal(sendctl)
			ctx.MMQServer.Publish("control", flysend)
		}
		//gen day statics
		cmp = strings.Compare(ctlitem.Cmd, "day")
		if cmp == 0 {
			fmt.Println("Gen Yestday Statistics !")
			now := time.Now()
			year, month, day := now.Date()

			// 今日日期
			today := time.Date(year, month, day, 0, 0, 0, 0, time.Local)
			fmt.Println("今日日期:", today)

			// 昨日日期
			yesterdaytime := today.AddDate(0, 0, -1)
			yesterday := yesterdaytime.Format("2006-01-02")
			if len(ctlitem.Data) > 0 {

				layout := "2006-01-02"

				yesterdaytime, _ = time.Parse(layout, ctlitem.Data)
				yesterday = ctlitem.Data
			}

			fmt.Println("昨日日期:", yesterday)
			sctx := context.Background()

			var uavStatistic uavlient.UavsStatistics

			history, err := ctx.MyRedis.Hget("history", yesterday)
			historyC := []byte(history) // strB len: 8, cap: 8

			if err != nil {
				fmt.Printf("parse  err:%s\n", err)
			} else {
				json.Unmarshal(historyC, &uavStatistic)

			}
			fmt.Printf("MakeStatistics---->  data:%s --> %s\n", yesterday, history)

			//get Snapshot

			person := []string{}
			all, err3 := ctx.UavMMQModel.FindCount(sctx, 0, yesterday, 5)
			if err3 != nil {
				fmt.Printf("FindCount  err:%s\n", err3)
			} else {
				for _, dict := range *all {
					person = append(person, dict.Image)
				}
			}

			bicycle := []string{}
			all, err3 = ctx.UavMMQModel.FindCount(sctx, 1, yesterday, 5)
			if err3 != nil {
				fmt.Printf("FindCount  err:%s\n", err3)
			} else {
				for _, dict := range *all {
					bicycle = append(bicycle, dict.Image)
				}
			}

			car := []string{}
			all, err3 = ctx.UavMMQModel.FindCount(sctx, 2, yesterday, 5)
			if err3 != nil {
				fmt.Printf("FindCount  err:%s\n", err3)
			} else {
				for _, dict := range *all {
					car = append(car, dict.Image)
				}
			}

			boxtruck := []string{}
			all, err3 = ctx.UavMMQModel.FindCount(sctx, 3, yesterday, 5)
			if err3 != nil {
				fmt.Printf("FindCount  err:%s\n", err3)
			} else {
				for _, dict := range *all {
					boxtruck = append(boxtruck, dict.Image)
				}
			}
			truck := []string{}
			all, err3 = ctx.UavMMQModel.FindCount(sctx, 4, yesterday, 5)
			if err3 != nil {
				fmt.Printf("FindCount  err:%s\n", err3)
			} else {
				for _, dict := range *all {
					truck = append(truck, dict.Image)
				}
			}

			tricycle := []string{}
			all, err3 = ctx.UavMMQModel.FindCount(sctx, 5, yesterday, 5)
			if err3 != nil {
				fmt.Printf("FindCount  err:%s\n", err3)
			} else {
				for _, dict := range *all {
					tricycle = append(tricycle, dict.Image)
				}
			}

			bus := []string{}
			all, err3 = ctx.UavMMQModel.FindCount(sctx, 6, yesterday, 5)
			if err3 != nil {
				fmt.Printf("FindCount  err:%s\n", err3)
			} else {
				for _, dict := range *all {
					bus = append(bus, dict.Image)
				}
			}

			motorcycle := []string{}
			all, err3 = ctx.UavMMQModel.FindCount(sctx, 7, yesterday, 5)
			if err3 != nil {
				fmt.Printf("FindCount  err:%s\n", err3)
			} else {
				for _, dict := range *all {
					motorcycle = append(motorcycle, dict.Image)
				}
			}

			fire := []string{}
			all, err3 = ctx.UavMMQModel.FindCount(sctx, 8, yesterday, 5)
			if err3 != nil {
				fmt.Printf("FindCount  err:%s\n", err3)
			} else {
				for _, dict := range *all {
					fire = append(fire, dict.Image)
				}
			}

			smoke := []string{}
			all, err3 = ctx.UavMMQModel.FindCount(sctx, 9, yesterday, 5)
			if err3 != nil {
				fmt.Printf("FindCount  err:%s\n", err3)
			} else {
				for _, dict := range *all {
					smoke = append(smoke, dict.Image)
				}
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
					Day:        yesterdaytime,
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

		var flydata uavlient.UavFlyData
		flydata.Cmd = "day"
		flysend, _ := json.Marshal(flydata)
		ctx.MMQServer.Publish("fly_control", flysend)

	})

	time.Sleep(2 * time.Second)

	// runAI("rtsp://127.0.0.1:5554/live/test", "uploads", "1")

	//start uav
	var flydata uavlient.UavFlyData
	flydata.Cmd = "start_uav"

	flysend, _ := json.Marshal(flydata)
	ctx.MMQServer.Publish("fly_control", flysend)

	//start camera ai
	flydata.Cmd = "start_ai"
	flysend, _ = json.Marshal(flydata)
	ctx.MMQServer.Publish("fly_control", flysend)

	//start corn timer
	flydata.Cmd = "corn"
	flysend, _ = json.Marshal(flydata)
	ctx.MMQServer.Publish("fly_control", flysend)

	fmt.Printf("Starting uav rpc server at %s...\n", c.ListenOn)
	s.Start()
}
