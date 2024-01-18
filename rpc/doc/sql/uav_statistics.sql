create table uav_statistics
(
    id           bigint auto_increment comment '编号' primary key,
    total        bigint                         not null comment '报警总数',
    remark       varchar(100)                        null comment '备注',
    person       bigint                         not null comment '人类报警',
    car          bigint                         not null comment '车辆报警',
    bus          bigint                         not null comment '卡车报警',
    snapshots    varchar(512)                        null comment '报警图列表',
    create_time  timestamp default CURRENT_TIMESTAMP null comment '统计时间',
)
comment '无人机巡检历史记录';

