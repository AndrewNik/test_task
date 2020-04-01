create table shop_delivery_point
(
	shop_id int not null,
	delivery_point_id int not null,
	primary key (shop_id, delivery_point_id),
	constraint shop_delivery_point_delivery_point_id_fk
		foreign key (delivery_point_id) references delivery_point (id)
			on update cascade on delete cascade,
	constraint shop_delivery_point_shop_id_fk
		foreign key (shop_id) references shop (id)
			on update cascade on delete cascade
);

