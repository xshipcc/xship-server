create table sms_coupon
(
    id            bigint auto_increment
        primary key,
    type          int(1)         not null comment '优惠券类型；0->全场赠券；1->会员赠券；2->购物赠券；3->注册赠券',
    name          varchar(100)   not null comment '名称',
    platform      int(1)         not null comment '使用平台：0->全部；1->移动；2->PC',
    count         int            not null comment '数量',
    amount        decimal(10, 2) not null comment '金额',
    per_limit     int            not null comment '每人限领张数',
    min_point     decimal(10, 2) not null comment '使用门槛；0表示无门槛',
    start_time    datetime       not null comment '开始时间',
    end_time      datetime       not null comment '结束时间',
    use_type      int(1)         not null comment '使用类型：0->全场通用；1->指定分类；2->指定商品',
    note          varchar(200)   not null comment '备注',
    publish_count int            not null comment '发行数量',
    use_count     int            not null comment '已使用数量',
    receive_count int            not null comment '领取数量',
    enable_time   datetime       not null comment '可以领取的日期',
    code          varchar(64)    not null comment '优惠码',
    member_level  int(1)         not null comment '可领取的会员类型：0->无限时'
)
    comment '优惠券表';

INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (2, 0, '全品类通用券', 0, 92, 10.00, 1, 100.00, '2018-08-27 16:40:47', '2018-11-23 16:40:47', 0, '满100减10', 100, 0, 8, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (3, 0, '小米手机专用券', 0, 92, 50.00, 1, 1000.00, '2018-08-27 16:40:47', '2018-11-16 16:40:47', 2, '小米手机专用优惠券', 100, 0, 8, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (4, 0, '手机品类专用券', 0, 92, 300.00, 1, 2000.00, '2018-08-27 16:40:47', '2018-09-15 16:40:47', 1, '手机分类专用优惠券', 100, 0, 8, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (7, 0, 'T恤分类专用优惠券', 0, 93, 50.00, 1, 500.00, '2018-08-27 16:40:47', '2018-08-15 16:40:47', 1, '满500减50', 100, 0, 7, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (8, 0, '新优惠券', 0, 100, 100.00, 1, 1000.00, '2018-11-08 00:00:00', '2018-11-27 00:00:00', 0, '测试', 100, 0, 1, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (9, 0, '全品类通用券', 0, 100, 5.00, 1, 100.00, '2018-11-08 00:00:00', '2018-11-10 00:00:00', 0, '测试', 100, 0, 1, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (10, 0, '全品类通用券', 0, 100, 15.00, 1, 200.00, '2018-11-08 00:00:00', '2018-11-10 00:00:00', 0, '测试', 100, 0, 1, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (11, 0, '全品类通用券', 0, 1000, 50.00, 1, 1000.00, '2018-11-08 00:00:00', '2018-11-10 00:00:00', 0, '测试', 1000, 0, 0, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (12, 0, '移动端全品类通用券', 1, 1, 10.00, 1, 100.00, '2018-11-08 00:00:00', '2018-11-10 00:00:00', 0, '测试', 100, 0, 0, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (19, 0, '手机分类专用', 0, 100, 100.00, 1, 1000.00, '2018-11-09 00:00:00', '2018-11-17 00:00:00', 1, '手机分类专用', 100, 0, 0, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (20, 0, '小米手机专用', 0, 100, 200.00, 1, 1000.00, '2018-11-09 00:00:00', '2018-11-24 00:00:00', 2, '小米手机专用', 100, 0, 0, '2021-03-16 21:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (21, 0, 'xxx11', 0, 100, 10.02, 1, 100.00, '2018-11-10 08:00:00', '2018-12-25 08:00:00', 2, '测试', 100, 0, 0, '2021-03-18 05:06:58', '0000', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (23, 0, '有效期测试', 0, 100, 10.00, 1, 100.00, '2019-10-05 16:00:00', '2023-04-26 07:41:29', 0, '测试', 100, 0, 0, '2021-03-17 13:06:58', 'string', 0);
INSERT INTO sms_coupon (id, type, name, platform, count, amount, per_limit, min_point, start_time, end_time, use_type, note, publish_count, use_count, receive_count, enable_time, code, member_level) VALUES (25, 0, '小米测试', 0, 10, 100.00, 100, 10.00, '2023-04-20 15:57:24', '2023-05-25 15:57:26', 0, '123', 10, 0, 0, '2023-05-25 15:57:26', '213', 0);
