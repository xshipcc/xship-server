create table uav_statistics
(
    day          DATE                           PRIMARY KEY comment '日期',
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
    remark       varchar(100)                       not null comment '备注',
    snapshots    varchar(1024)                     not  null comment '报警图列表'
)
comment '无人巡检每日记录';

