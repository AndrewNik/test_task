from tornado.web import RequestHandler, Application
from tornado.ioloop import IOLoop
from DBRequests import DBRequest
from datetime import datetime

connection_config = {
	'username': 'root',
	'password': '12345678',
	'host': 'localhost',
	'port': '3306',
	'database': 'test_task'
}

database = DBRequest(connection_config)


class BaseHandler(RequestHandler):
	def set_default_headers(self):
		self.set_header("Access-Control-Allow-Origin", "*")
		self.set_header("Access-Control-Allow-Headers", "x-requested-with")
		self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')

	def initialize(self, db):
		self.db = db


class Shop(BaseHandler):
	# /shops/shop_id
	def get(self, shop_id):
		result = self.db.shop_info(shop_id)
		self.write(str(result))

	def post(self, _):
		# POST data = {name: shop_name, domain: shop_domain}
		shop_name, shop_domain = self.get_argument('name', None), self.get_argument('domain', None)
		if shop_name and shop_domain:
			self.db.create_shop(shop_name, shop_domain)

	def put(self, shop_id):
		# PUT data = {name: shop_name, domain: shop_domain}
		shop_name, shop_domain = self.get_argument('name', None), self.get_argument('domain', None)
		if shop_name and shop_domain:
			self.db.update_shop(id=shop_id, name=shop_name, domain=shop_domain)


class DeliveryPoint(BaseHandler):
	def get(self, _):
		filter_type = self.get_argument('filter', None)
		# http://127.0.0.1:8888/delivery-points?filter=datetime&datetime=31/03/2020T11:02:00
		if filter_type == 'datetime' and self.get_argument('datetime', None):
			[str_date, time] = self.get_argument('datetime', None).split('T')
			date = datetime.strptime(str_date, '%d/%m/%Y')
			result = self.db.working_delivery_points(date.weekday(), time)
		# http://127.0.0.1:8888/delivery-points?filter=position&lat=55.820870&long=37.949635
		elif filter_type == 'position' and self.get_argument('lat') and self.get_argument('long'):
			latitude, longitude = self.get_argument('lat'), self.get_argument('long')
			result = self.db.nearby_delivery_points(latitude, longitude)
		else:
			result = self.db.delivery_points()
		self.write(str(result))

	def put(self, dp_id):
		# PUT data = {name: dp_name, address: dp_address, latitude: dp_latitude, longitude: dp_longitude}
		[name, address, lat, long] = map(lambda arg: self.get_argument(arg, None),
		                                 ['name', 'address', 'latitude', 'longitude'])
		if name and address and lat and long:
			self.db.update_delivery_point(id=dp_id, name=name, address=address, latitude=lat, longitude=long)

	# /delivery-points/dp_id
	def delete(self, dp_id):
		self.db.delete_delivery_point(dp_id)

	def post(self, _):
		# POST data = {name: dp_name, address: dp_address, latitude: dp_latitude, longitude: dp_longitude}
		[name, address, lat, long] = map(lambda arg: self.get_argument(arg, None),
		                                 ['name', 'address', 'latitude', 'longitude'])
		if name and address and lat and long:
			self.db.create_delivery_point(name, address, lat, long)


class ShopDeliveryPoint(BaseHandler):
	# POST data = {shop_id: some shop id, dp_id: some dp id}
	def post(self):
		shop_id, dp_id = self.get_argument('shop_id', None), self.get_argument('dp_id', None)
		if shop_id and dp_id:
			self.db.bind_dp_to_shop(shop_id, dp_id)


def make_app():
	urls = [
		("/shops/?(\d+)?", Shop, dict(db=database)),
		("/delivery-points/?(\d+)?", DeliveryPoint, dict(db=database)),
		("/shops-delivery-points", ShopDeliveryPoint, dict(db=database))]
	return Application(urls, debug=True)


app = make_app()
app.listen(8888)
IOLoop.current().start()
