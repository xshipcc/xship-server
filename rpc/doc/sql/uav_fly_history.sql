create table uav_fly_history
(
    id                bigint auto_increment comment '编号' primary key,
    uav_id         bigint                              not null comment '无人机id',
    uav_name          varchar(16)                          not null comment '无人机名称',
    fly_id        bigint                              not null comment '巡检路线id',
    road_name          varchar(16)                          not null comment '无人机名称',
    path          varchar(32)                          not null comment '录像存储路径',
    operator       varchar(16)                        not null comment '操作者',
    status       bigint                         not null comment '-1,异常结束，0->起飞；1->正常完成',
    remark      varchar(100)                     not  null comment '异常结束原因',
    fly_data        varchar(10240)                        not null comment '路线数据',
    lat    double                                 not null comment '纬度',
    lon    double                                 not null comment '经度',
    alt    double                                 not null comment '高度',
    create_time    timestamp default CURRENT_TIMESTAMP null comment '飞行开始时间',
    end_time       timestamp default CURRENT_TIMESTAMP null comment '飞行结束时间'
)
comment '无人机巡检历史记录';

