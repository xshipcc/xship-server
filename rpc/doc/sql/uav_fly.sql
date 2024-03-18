create table uav_fly
(
    id       bigint auto_increment comment '路线编号'
        primary key,
    name   varchar(150)                        not null UNIQUE comment '路线昵称',
    data       varchar(10240)                        not null comment '路线数据',
    create_time       timestamp default CURRENT_TIMESTAMP not null comment '创建时间',
    creator       varchar(16)                        not null comment '创建者'
)
 comment '无人机飞行路线设计';