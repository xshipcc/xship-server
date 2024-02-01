create table uav_device
(
    id                bigint auto_increment comment '无人机id'
        primary key,
    name        varchar(150)                 not null UNIQUE comment '无人机名称',
    ip          varchar(256)                 not null comment '无人机IP',
    port        bigint                       not null comment '无人机port',
    uav_zubo       bigint                        not null comment ' 无人机:0->单播；1->组播',
    r_port        bigint                       not null comment '无人机接收端口port',
    hangar_ip       varchar(256)                        not null comment '无人机机库IP',
    hangar_port       bigint                       not null comment '无人机机库port',
    hangar_rport       bigint                       not null comment '无人机机库接收port',
    hangar_zubo       bigint                        not null comment ' 机库:0->单播；1->组播',
    cam_ip       varchar(256)                        not null comment '摄像头IP',
    cam_port     bigint                       not null comment '摄像头port',
    cam_zubo       bigint                        not null comment ' 摄像头:0->单播；1->组播',
    cam_url      varchar(256)                       not null comment '摄像头rtsp 地址',
    create_time       timestamp default CURRENT_TIMESTAMP null comment '创建时间',
    network      varchar(64)                 not null comment '网卡配置',  
    joystick      varchar(64)                 not null comment '手柄配置',  
    status       bigint                        not null comment ' 帐号启用状态:0->禁用；1->启用'

)
 comment '无人机飞行设置';

