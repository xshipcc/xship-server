create table uav_people
(
    id                bigint auto_increment comment '编号'
        primary key,
    username       varchar(16)               not null comment '人名称',
    icon       varchar(200)                  not null comment '人头像',
    level       bigint                        not null comment '等级分类 人员等级 本部,0，外来 1，工程 1',
    phone       varchar(16)                  not null comment '手机号码',
    status       bigint                        not null comment ' 帐号启用状态:0->禁用；1->启用',
    gender       bigint                        not null comment '  性别：0->未知；1->男；2->女',
    create_time    timestamp default CURRENT_TIMESTAMP null comment '飞行开始时间'
)
comment '无人机人员头像记录';

