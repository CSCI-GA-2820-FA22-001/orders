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
	
