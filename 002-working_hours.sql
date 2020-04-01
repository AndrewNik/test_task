create table working_hours
(
	id int auto_increment
		primary key,
	week_day int not null,
	opening_time time not null,
	closing_time time not null,
	break_start time null,
	break_end time null,
	delivery_point_id int not null,
	constraint delivery_point_id__fk
		foreign key (delivery_point_id) references delivery_point (id)
			on update cascade on delete cascade
);

