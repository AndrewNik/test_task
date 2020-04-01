create table shop
(
	id int auto_increment
		primary key,
	name varchar(255) charset utf8 not null,
	domain varchar(255) charset utf8 not null,
	constraint shop_domain_uindex
		unique (domain)
);

