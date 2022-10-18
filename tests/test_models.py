"""
Test cases for YourResourceModel Model

"""
import os
import logging
import unittest

from importlib_metadata import metadata
from service import app
from service.models import Order, DataValidationError, db, Items
from service.config import DATABASE_URI


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
		order = Order(user_id=123, create_time="2022-10-16", status=1)
		order.create()
		self.assertEqual(str(order), "<User 123 Create Time=2022-10-16 Status=1>")
		self.assertTrue(order is not None)
		self.assertEqual(order.user_id, 123)
		self.assertEqual(order.create_time, "2022-10-16")
		self.assertEqual(order.status, 1)
		# Test create
		db_order = Order.find(order.id)
		self.assertEqual(str(db_order), "<User 123 Create Time=2022-10-16 Status=1>")
		self.assertTrue(db_order is not None)
		self.assertEqual(db_order.user_id, 123)
		self.assertEqual(db_order.id, order.id)
		self.assertEqual(db_order.create_time, "2022-10-16")
		self.assertEqual(db_order.status, 1)

		bad_order = Order.find(order.id+1)
		self.assertTrue(bad_order is None)

	def test_delete_order(self):
		"""test delete function in Order"""
		order = Order(user_id=123, create_time="2022-10-16", status=1)
		order.create()
		order_id = order.id
		order.delete()
		db_order = Order.find(order_id)
		self.assertEqual(db_order, None)

	def test_update_order(self):
		"""test update function in Order"""
		order = Order(user_id=123, create_time="2022-10-16", status=1)
		order.create()
		order.user_id = 234
		order.create_time = "2021-1-2"
		order.status = 0
		order.update()
		db_order = Order.find(order.id)
		self.assertTrue(db_order is not None)
		self.assertEqual(db_order.user_id, 234)
		self.assertEqual(db_order.create_time, "2021-1-2")
		self.assertEqual(db_order.status, 0)

	def test_serialize_order(self):
		"""test serialize"""
		order = Order(user_id=123, create_time="2022-10-16", status=1)
		test_dict = {"id": None, "user_id": 123, "create_time": "2022-10-16", "status": 1}
		self.assertEqual(order.serialize(), test_dict)

	def test_deserialize_order(self):
		"""test deserialize order"""
		order = Order()
		init_dict = {"user_id": 123, "create_time": "2021-10-16", "status": 0}
		bad_dic_1 = {"user_id": 123, "create_time": "2021-10-16"}
		bad_dic_2 = {"create_time": "2021-10-16", "status": 0}
		bad_dic_3 = {"user_id": 123, "status": 0}
		bad_dic_4 = {"user_id": "bad userid", "create_time": 20140103, "status": "bad status"}
		bad_dic_5 = {"user_id": 123, "create_time": 20140103, "status": 0}
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
		self.assertEqual(updated_order.create_time, "2021-10-16")
		self.assertEqual(updated_order.status, 0)

	def test_list_all_order(self):
		"""test serialize"""
		self.assertEqual(Order.all(), [])
		order1 = Order(user_id=123, create_time="2022-10-16", status=1)
		order2 = Order(user_id=124, create_time="2022-10-6", status=1)
		order3 = Order(user_id=125, create_time="2022-10-5", status=1)
		order1.create()
		order2.create()
		order3.create()
		self.assertEqual(len(Order.all()), 3)

	def test_find_by_user_id(self):
		"""test find by user id"""
		order1 = Order(user_id=123, create_time="2022-10-16", status=1)
		order2 = Order(user_id=123, create_time="2022-10-6", status=1)
		order3 = Order(user_id=123, create_time="2022-10-5", status=1)
		order1.create()
		order2.create()
		order3.create()
		found = Order.find_by_user_id(123)
		self.assertEqual(found.count(), 3)
		for order in found:
			self.assertEqual(order.user_id, 123)

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
	
	def test_item_find(self):
		"""test item find"""
		order1 = Order(user_id=123, create_time="2021-10-10", status=1)
		order2 = Order(user_id=124, create_time="2021-10-11", status=1)
		order1.create()
		order2.create()
		item1 = Items(order_id=order1.id, item_id= 1)
		item2 = Items(order_id=order1.id, item_id =2)
		item3 = Items(order_id=order2.id, item_id =2)
		item1.create()
		item2.create()
		item3.create()
		found = Items.find_by_order_id(order1.id)
		for item in found:
			self.assertEqual(item.order_id, order1.id)
		found = Items.find_by_order_id(order2.id)
		for item in found:
			self.assertEqual(item.order_id, order2.id)