create table uav_plan
(
    id                bigint auto_increment comment '编号'
        primary key,
    uav_id         bigint                              not null comment '无人机id',
    plan       varchar(256)                        not null comment '定时字符串',
    fly_id        bigint                              not null comment '巡检路线id',
    create_time       timestamp default CURRENT_TIMESTAMP null comment '飞行开始时间'
)
comment '无人机巡检计划';

