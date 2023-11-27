create table uav_fly_history_detail
(
    id                bigint auto_increment comment '编号'  primary key,
    history_id         bigint                              not null comment '飞行id',
    temp         tinyint                              not null comment '温度',
    eng         tinyint                              not null comment '功耗',
    v         decimal(10, 2)                              not null comment '电压',
    a         decimal(10, 2)                              not null comment '电流',
    stay_time         decimal(10, 2)                              not null comment '悬停时间',
    gps_stars         tinyint                              not null comment 'GPS星数',
    toward_angle    double                                 not null comment '方向角',
    lat    double                                 not null comment '纬度',
    lon    double                                 not null comment '经度',
    staus         int                              not null comment '状态',
    height    float                                 not null comment '高度',
    speed    float                                 not null comment '速度',
    rel_height    float                                 not null comment '相对原点高度',
    real_height    float                                 not null comment '实时距地高度',
    current    timestamp default CURRENT_TIMESTAMP null comment '当前时间'
)

comment '无人机巡检历史记录_详情点位数据';

