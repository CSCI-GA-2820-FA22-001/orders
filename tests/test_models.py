"""
Test cases for YourResourceModel Model
"""
import logging
import unittest
from flask import jsonify
from service import app
from service.models import Order, DataValidationError, db, Items, Status
from service.config import DATABASE_URI
from time import time

######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################


class TestOrderModel(unittest.TestCase):
	""" Test Cases for Order Model """

	@classmethod
	def setUpClass(cls):
		""" This runs once before the entire test suite """
		app.config["TESTING"] = True
		app.config["DEBUG"] = False
		app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
		app.logger.setLevel(logging.CRITICAL)
		Order.init_db(app)

	@classmethod
	def tearDownClass(cls):
		""" This runs once after the entire test suite """
		db.session.close()

	def setUp(self):
		""" This runs before each test """
		db.session.query(Order).delete()  # clean up the last tests
		db.session.query(Items).delete()
		db.session.commit()

	def tearDown(self):
		""" This runs after each test """
		db.session.remove()

	######################################################################
	#  T E S T   C A S E S
	######################################################################

	def test_create_order(self):
		""" It should always be true """
		# Test constructor
		ts = (int)(time())
		order = Order(user_id=123, create_time=ts, status=Status.CREATED)
		order.create()
		self.assertEqual(str(order), f"<User 123 Create Time={ts} Status=1>")
		self.assertTrue(order is not None)
		self.assertEqual(order.user_id, 123)
		self.assertEqual(order.create_time, ts)
		self.assertEqual(order.status, 1)
		# Test create
		db_order = Order.find(order.id)
		self.assertEqual(str(db_order), f"<User 123 Create Time={ts} Status=1>")
		self.assertTrue(db_order is not None)
		self.assertEqual(db_order.user_id, 123)
		self.assertEqual(db_order.id, order.id)
		self.assertEqual(db_order.create_time, ts)
		self.assertEqual(db_order.status, 1)

		# Test for loop Items create
		info = {
			"order_id": order.id,
			"items": [1,2,3]
		}
		for item_id in jsonify(info).get_json().get("items"):
			items = Items()
			items.order_id = order.id
			items.item_id = item_id
			items.create()
		found = Items.find_by_order_id(order.id)
		item_list = [item for item in found]
		count = len(item_list)
		self.assertEqual(count, 3)
		self.assertEqual(found[2].order_id, order.id)
		self.assertEqual(found[2].item_id, 3)

		bad_order = Order.find(order.id + 1)
		self.assertTrue(bad_order is None)

	def test_delete_order(self):
		"""test delete function in Order"""
		order = Order(user_id=123, create_time=(int)(time()), status=Status.CREATED)
		order.create()
		order_id = order.id
		order.delete()
		db_order = Order.find(order_id)
		self.assertEqual(db_order, None)

	def test_update_order(self):
		"""test update function in Order"""
		ts = (int)(time())
		order = Order(user_id=123, create_time=ts, status=Status.CREATED)
		order.create()
		order.user_id = 234
		ts1 = (int)(time())
		order.create_time = ts1
		order.status = Status.CANCELLED
		order.update()
		db_order = Order.find(order.id)
		self.assertTrue(db_order is not None)
		self.assertEqual(db_order.user_id, 234)
		self.assertEqual(db_order.create_time, ts1)
		self.assertEqual(db_order.status, Status.CANCELLED)

	def test_serialize_order(self):
		"""test serialize"""
		order = Order(user_id=123, create_time="2022-10-16", status=Status.CREATED)
		test_dict = {"id": None, "user_id": 123, "create_time": "2022-10-16", "status": Status.CREATED}
		self.assertEqual(order.serialize(), test_dict)

	def test_deserialize_order(self):
		"""test deserialize order"""
		order = Order()
		init_dict = {"user_id": 123, "create_time": 20140103, "status": Status.CREATED}
		bad_dic_1 = {"user_id": 123, "create_time": "2021-10-16"}
		bad_dic_2 = {"create_time": "2021-10-16", "status": Status.CREATED}
		bad_dic_3 = {"user_id": 123, "status": Status.CREATED}
		bad_dic_4 = {"user_id": "bad userid", "create_time": 20140103, "status": "bad status"}
		bad_dic_5 = {"user_id": 123, "create_time": "2021-10-16", "status": Status.CREATED}
		bad_dic_6 = {"user_id": 123, "create_time": "2021-10-16", "status": "bad status"}
		with self.assertRaises(DataValidationError):
			order.deserialize(bad_dic_1)
		with self.assertRaises(DataValidationError):
			order.deserialize(bad_dic_2)
		with self.assertRaises(DataValidationError):
			order.deserialize(bad_dic_3)
		with self.assertRaises(DataValidationError):
			order.deserialize(bad_dic_4)
		with self.assertRaises(DataValidationError):
			order.deserialize(bad_dic_5)
		with self.assertRaises(DataValidationError):
			order.deserialize(bad_dic_6)
		updated_order = order.deserialize(init_dict)
		self.assertEqual(updated_order.user_id, 123)
		self.assertEqual(updated_order.create_time, 20140103)
		self.assertEqual(updated_order.status, Status.CREATED)

	def test_list_all_order(self):
		"""test list all order"""
		self.assertEqual(Order.all(), [])
		order1 = Order(user_id=123, create_time=(int)(time()), status=1)
		order2 = Order(user_id=124, create_time=(int)(time()), status=1)
		order3 = Order(user_id=125, create_time=(int)(time()), status=1)
		order1.create()
		order2.create()
		order3.create()
		self.assertEqual(len(Order.all()), 3)

	def test_find_by_user_id(self):
		"""test find by user id"""
		order1 = Order(user_id=123, create_time=(int)(time()), status=1)
		order2 = Order(user_id=123, create_time=(int)(time()), status=1)
		order3 = Order(user_id=123, create_time=(int)(time()), status=1)
		order1.create()
		order2.create()
		order3.create()
		found = Order.find_by_user_id(123)
		self.assertEqual(found.count(), 3)
		for order in found:
			self.assertEqual(order.user_id, 123)

	def test_find_by_create_time(self):
		"""test find by user id"""
		order1_time = 100
		order1 = Order(user_id=1, create_time=order1_time, status=1)
		order2_time = 200
		order2 = Order(user_id=2, create_time=order2_time, status=1)
		order3_time = 300
		order3 = Order(user_id=3, create_time=order3_time, status=1)
		order1.create()
		order2.create()
		order3.create()
		found = Order.find_by_create_time(order1_time)
		self.assertEqual(found.count(), 1)
		for order in found:
			self.assertEqual(order.user_id, 1)

	def test_find_by_status(self):
		"""test find by status"""
		ts = int(time())
		order1 = Order(user_id=1, create_time=ts, status=1)
		order2 = Order(user_id=1, create_time=ts, status=2)
		order3 = Order(user_id=1, create_time=ts, status=3)
		order4 = Order(user_id=1, create_time=ts, status=1)
		order1.create()
		order2.create()
		order3.create()
		order4.create()
		found1 = Order.find_by_status(1, 1)
		self.assertEqual(found1.count(), 2)
		found2 = Order.find_by_status(1, 2)
		self.assertEqual(found2.count(), 1)
		found3 = Order.find_by_status(1, 3)
		self.assertEqual(found3.count(), 1)
		found4 = Order.find_by_status(2, 3)
		self.assertEqual(found4.count(), 0)


class TestItemsModel(unittest.TestCase):
	""" Test Cases for Items Model """

	@classmethod
	def setUpClass(cls):
		""" This runs once before the entire test suite """
		app.config["TESTING"] = True
		app.config["DEBUG"] = False
		app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
		app.logger.setLevel(logging.CRITICAL)
		Order.init_db(app)
		Items.init_db(app)

	@classmethod
	def tearDownClass(cls):
		""" This runs once after the entire test suite """
		db.session.close()

	def setUp(self):
		""" This runs before each test """
		db.session.query(Items).delete()  # clean up the last tests
		db.session.query(Order).delete()
		db.session.commit()

	def tearDown(self):
		""" This runs after each test """
		db.session.remove()

	######################################################################
	#  T E S T   C A S E S
	######################################################################

	def test_item_repr(self):
		"""test item __repr__"""
		order = Order(user_id=123, create_time=(int)(time()), status=Status.CREATED)
		order.create()
		item = Items(order_id=order.id, item_id=1)
		item.create()
		self.assertEqual(str(item), f"<Order id=[{item.order_id}] Item id=[{item.item_id}]>")

	def test_item_find(self):
		"""test item find"""
		ts = (int)(time())
		order1 = Order(user_id=123, create_time=ts, status=Status.CREATED)
		order2 = Order(user_id=124, create_time=ts, status=Status.CREATED)
		order1.create()
		order2.create()
		item1 = Items(order_id=order1.id, item_id=1)
		item2 = Items(order_id=order1.id, item_id=2)
		item3 = Items(order_id=order2.id, item_id=2)
		item1.create()
		item2.create()
		item3.create()
		found = Items.find_by_order_id(order1.id)
		for item in found:
			self.assertEqual(item.order_id, order1.id)
		found = Items.find_by_order_id(order2.id)
		for item in found:
			self.assertEqual(item.order_id, order2.id)
		found1 = Items.find_by_item_id(1)
		for item in found1:
			self.assertEqual(item.item_id, 1)
		found2 = Items.find_by_item_id(2)
		for item in found2:
			self.assertEqual(item.item_id, 2)

	def test_item_update(self):
		"""test item update"""
		order = Order(user_id=123, create_time=(int)(time()), status=Status.CREATED)
		order.create()
		item = Items(order_id=order.id, item_id=1)
		item.create()
		item.item_id = 10
		item.update()
		self.assertEqual(Items.find(item.id).item_id, 10)

	def test_deserialize_item(self):
		"""test deserialize order"""
		item = Items()
		init_dict = {"order_id": 123, "item_id": 999}
		bad_dic_1 = {"order_id": 123}
		bad_dic_2 = {"item_id": 123}
		bad_dic_3 = {"order_id": "bad order_id", "item_id": 999}
		bad_dic_4 = {"order_id": 123, "item_id": "bad item_id"}
		bad_dic_5 = {"order_id": "bad order_id", "item_id": "bad item_id"}

		with self.assertRaises(DataValidationError):
			item.deserialize(bad_dic_1)
		with self.assertRaises(DataValidationError):
			item.deserialize(bad_dic_2)
		with self.assertRaises(DataValidationError):
			item.deserialize(bad_dic_3)
		with self.assertRaises(DataValidationError):
			item.deserialize(bad_dic_4)
		with self.assertRaises(DataValidationError):
			item.deserialize(bad_dic_5)

		updated_item = item.deserialize(init_dict)
		self.assertEqual(updated_item.order_id, 123)
		self.assertEqual(updated_item.item_id, 999)

	def test_item_all(self):
		"""test all item function"""
		order1 = Order(user_id=123, create_time=(int)(time()), status=Status.CREATED)
		order1.create()
		item1 = Items(order_id=order1.id, item_id=1)
		item2 = Items(order_id=order1.id, item_id=2)
		item3 = Items(order_id=order1.id, item_id=2)
		item1.create()
		item2.create()
		item3.create()
		found = Items.all()
		self.assertEqual(len([item for item in found]), 3)
