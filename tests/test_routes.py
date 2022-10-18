"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
  nosetests -v --with-spec --spec-color
  coverage report -m
"""
from ast import Or
import os
import logging
from flask import jsonify
from unittest import TestCase
from unittest.mock import MagicMock, patch
from service import app
from service.models import db, Order, Items
from service.common import status  # HTTP Status Codes
from .common import status

DATABASE_URI = os.getenv(
    "DATABASE_URI", "postgresql://postgres:postgres@localhost:5432/postgres"
)
BASE_URL = "/orders"
######################################################################
#  T E S T   C A S E S
######################################################################
class TestOrderServer(TestCase):
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
    #  H E L P E R S   F U N C T I O N S   H E R E
    ######################################################################

    def _create_order(self, user_id, create_time, s):
        info = {
            "user_id": user_id,
            "create_time": create_time,
            "status": status,
        }
        order = Order()
        order.deserialize(jsonify(info))
        resp = self.client.post(BASE_URL + "/orders", jsonify(info))
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            "Could not create test order",
        )
        order.id = resp.get_json()["id"]
        return order

    def _create_item(self, order_id, item_id):
        info = {
            "order_id": order_id,
            "item_id": item_id,
        }
        item = Items()
        item.deserialize(jsonify(info))
        resp = self.client.post(f"{BASE_URL}/orders/order_id/items", jsonify(info))
        self.assertEqual(
            resp.status_code,
            status.HTTP_201_CREATED,
            "Could not create test order item",
        )
        item.id = resp.get_json()["id"]
        return item


    ######################################################################
    #  P L A C E   T E S T   C A S E S   H E R E
    ######################################################################

    def test_index(self):
        """ It should call the home page """
        resp = self.client.get("/")
        # print(resp.)
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_list_orders(self):
        """ It should return a list of orders """
        order1 = Order()

