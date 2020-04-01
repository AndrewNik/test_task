from sqlalchemy.engine import create_engine
from sqlalchemy.engine.url import URL


class DBRequest:
	def __init__(self, cfg):
		self.engine = create_engine(URL('mysql', **cfg))
		self.connection = self.engine.connect()

	def shop_info(self, shop_id):
		result = self.connection.execute('SELECT name, domain FROM shop WHERE id="{}"'.format(shop_id)).fetchone()
		return result

	def create_shop(self, shop_name, shop_domain):
		self.connection.execute('INSERT INTO shop (name, domain) VALUES ("{}", "{}")'.format(shop_name, shop_domain))

	def update_shop(self, **kwargs):
		self.connection.execute(
			'INSERT INTO shop (id, name, domain)  VALUES("{id}", "{name}", "{domain}") ON DUPLICATE KEY UPDATE name = "{name}", domain = "{domain}"'.format(**kwargs))

	def update_delivery_point(self, **kwargs):
		self.connection.execute(
			"""INSERT INTO delivery_point (id, name, address, latitude, longitude) 
			VALUES('{id}', '{name}', '{address}', '{latitude}', '{longitude}') ON DUPLICATE KEY 
			UPDATE name = '{name}', address = '{address}', latitude = '{latitude}', longitude = '{longitude}'""".format(**kwargs))

	def delete_delivery_point(self, dp_id):
		self.connection.execute('DELETE FROM delivery_point WHERE id="{}"'.format(dp_id))

	def create_delivery_point(self, name, address, lat, long):
		self.connection.execute(
			'INSERT INTO delivery_point (name, address, latitude, longitude) VALUES ("{}","{}","{}","{}")'.format(name, address, lat, long))

	def bind_dp_to_shop(self, shop_id, dp_id):
		self.connection.execute(
			'INSERT INTO shop_delivery_point VALUES ({}, {})'.format(shop_id, dp_id))

	def delivery_points(self):
		return self.connection.execute(
			"""SELECT name, address, CONVERT(opening_time, CHAR),CONVERT(closing_time, CHAR), CONVERT(break_start, CHAR),
			 CONVERT(break_end, CHAR) FROM delivery_point dp JOIN working_hours wh on dp.id = wh.delivery_point_id""").fetchall()

	def working_delivery_points(self, weekday, time):
		return self.connection.execute(
			"""SELECT name, address, CONVERT(opening_time, CHAR),CONVERT(closing_time, CHAR), CONVERT(break_start, CHAR), CONVERT(break_end, CHAR) 
			FROM delivery_point dp JOIN working_hours wh on dp.id = wh.delivery_point_id WHERE dp.id IN 
			(SELECT delivery_point_id FROM working_hours WHERE (week_day = '{weekday}') AND ('{time}' BETWEEN opening_time AND closing_time)
			AND (IF(break_start IS NOT NULL AND break_end IS NOT NULL, '{time}' NOT BETWEEN break_start AND break_end, TRUE)))
			""".format(**{'weekday': weekday, 'time': time})
		).fetchall()

	def nearby_delivery_points(self, latitude, longitude):
		return self.connection.execute(
			"""SELECT name, address, CONVERT(opening_time, CHAR),CONVERT(closing_time, CHAR), CONVERT(break_start, CHAR), 
			CONVERT(break_end, CHAR), ST_Distance_Sphere(point(dp.longitude, dp.latitude),point({}, {})) as distance 
			FROM delivery_point dp JOIN working_hours wh on dp.id = wh.delivery_point_id ORDER BY distance;
			""".format(longitude, latitude)
		).fetchall()
