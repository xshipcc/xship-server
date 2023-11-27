create table uav_network
(
    id                bigint auto_increment comment '网络频段'
        primary key,
    name   varchar(150)                      not  null comment '网络频段名称',
    band       bigint                       not null comment '频段信息',
    type       bigint                       not null comment '频段类型',

    create_time       timestamp default CURRENT_TIMESTAMP null comment '飞行开始时间'
)
 comment '无人机网络频段';

