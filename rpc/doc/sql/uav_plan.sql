create table uav_plan
(
    id                bigint auto_increment comment '编号'
        primary key,
    name       varchar(16)               not null comment '名称',
    uav_id         bigint                not null comment '无人机id',
    fly_id        bigint                 not null comment '巡检路线id',
    plan       varchar(256)              not null comment '定时字符串',
    status       bigint                  not null comment ' 帐号启用状态:0->禁用；1->启用',

    create_time       timestamp default CURRENT_TIMESTAMP null comment '飞行开始时间'
)
comment '无人机巡检计划';

