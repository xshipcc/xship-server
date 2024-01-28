create table uav_camera
(
    id                bigint auto_increment comment '摄像头id' primary key,
    name        varchar(150)                 not null comment '摄像头名称',
    tunnel       bigint                 not null comment '通道',
    status       bigint                 not null comment '状态 启用，关闭，运行，离线',
    url          varchar(256)                       not null comment '摄像头地址多种信息',
    rtsp_url          varchar(256)                       not null comment '摄像头AI地址',

    platform                                int      not null comment '使用平台：0-全部 1-飞机 2-摄像头;3-机库;4-AI;5-交通岗',
    lat    double                                 not null comment '纬度',
    lon    double                                 not null comment '经度',
    alt    double                                 not null comment '高度',
    ai_status       bigint                  not null comment ' 摄像头AI 启用状态:0->禁用；1->启用',

    create_time       timestamp default CURRENT_TIMESTAMP null comment '创建时间'
)
 comment '摄像头设置';

