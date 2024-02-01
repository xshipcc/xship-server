create table uav_car
(
    id                bigint auto_increment comment '编号'primary key,
    name       varchar(16)               not null UNIQUE comment '人名称',
    card       varchar(200)                  not null comment '车牌号',
    photo       varchar(200)                  not null comment '车辆照片',
    type       bigint                        not null comment '等级分类 人员等级 本部,0，外来 1，工程 1',
    phone       varchar(16)                  not null comment '手机号码',
    status       bigint                        not null comment ' 帐号启用状态:0->禁用；1->启用',
    agency       varchar(32)                         not null comment '  所属机构名称',
    create_time    timestamp default CURRENT_TIMESTAMP null comment '注册时间'
)
comment '车辆系统记录';

