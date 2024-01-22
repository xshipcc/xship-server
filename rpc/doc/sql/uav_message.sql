create table uav_message
(
    id                          bigint auto_increment
        primary key,
    name                        varchar(64)  not null comment '报警标题',
    image                           varchar(64)       not null comment '报警截图',
    type                        int      not null comment '消息类型:0-发现人员 1-車輛 2-入侵 3-烟火 4-',
    code                        varchar(12)           not null comment '系统分类二级类别',
    level                       int      not null comment '预警等级',
    count                       int      not null comment '报警数量',
    platform                    int      not null comment '使用平台：0-全部 1-飞机 2-摄像头;3-机库;4-AI',
    lat                         double    not null comment '经度',
    lon                         double    not null comment '纬度',
    alt                         double    not null comment '高度',
    create_time    timestamp default CURRENT_TIMESTAMP not null comment '开始时间',
    note                         varchar(24)       not null comment '备注',
    history_id                   int      not null comment '巡检历史ID',
    confirm                      int      not null comment '报警确认'
)
    comment '报警列表';

