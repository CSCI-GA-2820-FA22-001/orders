"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
import os
import logging
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import db, Order, Items
from service.common import status  # HTTP Status Codes

DATABASE_URI = os.getenv(
	"DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/orders"
######################################################################
#  T E S T   C A S E S
######################################################################
class TestYourResourceServer(TestCase):
	""" REST API Server Tests """

	@classmethod
	def setUpClass(cls):
		""" This runs once before the entire test suite """
		app.config["TESTING"] = True
		app.config["DEBUG"] = False
		# Set up the test database
		app.config["SQLALCHEMY_DATABASE_URI"] = DATABASE_URI
		app.logger.setLevel(logging.CRITICAL)
		Order.init_db(app)

	@classmethod
	def tearDownClass(cls):
		""" This runs once after the entire test suite """
		db.session.close()

	def setUp(self):
		""" This runs before each test """
		self.client = app.test_client()
		db.session.query(Order).delete()  # clean up the last tests
		db.session.commit()

	def tearDown(self):
		""" This runs after each test """
		db.session.remove()

	######################################################################
	#  P L A C E   T E S T   C A S E S   H E R E
	######################################################################

	def test_index(self):
		""" It should call the home page """
		resp = app.get("/")
		# print(resp.)
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
	
	def test_create_order(self):
		""" It should Create a new Order"""
		test_order = Order()
		test_order.user_id = 0
		test_order.create_time = "2021/03/16 16:30:00"
		test_order.status = 0
		test_order.create()

		logging.debug("Test Order: %s", test_order.serialize())
		response = self.client.post(BASE_URL, json=test_order.serialize())
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		# Make sure location header is set
		location = response.headers.get("Location", None)
		self.assertIsNotNone(location)

		# Check the data is correct
		new_order = response.get_json()
		self.assertEqual(new_order["user_id"], test_order.user_id)
		self.assertEqual(new_order["create_time"], test_order.create_time)
		self.assertEqual(new_order["status"], test_order.status)

		# Check that the location header was correct
		response = self.client.get(location)
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		new_order = response.get_json()
		self.assertEqual(new_order["user_id"], test_order.user_id)
		self.assertEqual(new_order["create_time"], test_order.create_time)
		self.assertEqual(new_order["status"], test_order.status)

	
