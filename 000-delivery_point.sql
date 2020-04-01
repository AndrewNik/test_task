create table delivery_point
(
	id int auto_increment
		primary key,
	name varchar(255) charset utf8 not null,
	address varchar(255) charset utf8 not null,
	latitude decimal(10,8) not null,
	longitude decimal(11,8) not null
);

