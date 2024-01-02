create table uav_fly_history
(
    id                bigint auto_increment comment '编号'
        primary key,
    uav_id         bigint                              not null comment '无人机id',
    fly_id        bigint                              not null comment '巡检路线id',
    operator       varchar(16)                        not null comment '操作者',
    lat    double                                 not null comment '纬度',
    lon    double                                 not null comment '经度',
    create_time    timestamp default CURRENT_TIMESTAMP null comment '飞行开始时间',
    end_time       timestamp default CURRENT_TIMESTAMP null comment '飞行结束时间'
)
comment '无人机巡检历史记录';

