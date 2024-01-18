create table uav_statistics
(
    id           bigint auto_increment comment '编号' primary key,
    total        bigint                         not null comment '报警总数',
    person       bigint                         not null comment '人类报警',
    car          bigint                         not null comment '车辆报警',
    bicycle      bigint                         not null comment '自行车',
    bus          bigint                         not null comment '汽车',
    truck          bigint                         not null comment '卡车',
    box_truck    bigint                         not null comment '厢式货车',
    tricycle    bigint                         not null comment '三轮车',
    motorcycle    bigint                         not null comment '摩托车',
    smoke    bigint                         not null comment '烟雾',
    fire    bigint                         not null comment '火',
    remark       varchar(100)                        null comment '备注',
    snapshots    varchar(512)                        null comment '报警图列表',
    create_time  timestamp default CURRENT_TIMESTAMP null comment '统计时间',
)
comment '无人巡检每日记录';

