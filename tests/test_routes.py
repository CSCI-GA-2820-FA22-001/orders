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
from .factories import create_random_time_str

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
    
    def _create_order(self, count, user_id_incr = 0):
        """Factory method to create orders in bulk
        param:
            count -> int: represent how many orders you want to generate
            user_id_incr -> int: what is the difference between previous user id and next user id
        """
        orders = []
        user_id = 0
        for _ in range(count):
            order = Order(user_id=user_id, create_time=create_random_time_str(), status=0)
            orders.append(order)
            user_id += user_id_incr
        return orders


    def _create_order_by_info(self, user_id, create_time, stat):
        info = {
            "user_id": user_id,
            "create_time": create_time,
            "status": stat,
        }
        order = Order()
        order.deserialize(jsonify(info))
        resp = self.client.post(BASE_URL + "/orders", json=jsonify(info), content_type="application/json")
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
        resp = self.client.post(f"{BASE_URL}/orders/order_id/items", json=jsonify(info), content_type="application/json")
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
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
    
    def test_delete_order(self):
        """ test Delete /orders/<int:order_id>"""
        order = self._create_order(1, 1)[0]
        order.create()
        response = self.client.delete(f"{BASE_URL}/{order.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        db_order = Order.find(order.id)
        self.assertEqual(db_order, None)
        # Todo: get this item and check if it's none
    
    def test_delete_item(self):
        """ test delete item by order id and item id"""
        order1 = Order(user_id=123, create_time="2021-10-10", status=1)
        order1.create()
        item1 = Items(order_id=order1.id, item_id= 1)
        item2 = Items(order_id=order1.id, item_id =2)
        item1.create()
        item2.create()
        response = self.client.delete(f"{BASE_URL}/{order1.id}/items/{item1.id}")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        found = Items.find_by_order_id(order_id=order1.id)
        count = len([item for item in found])
        self.assertEqual(count, 1)
        self.assertEqual(found[0].id, item2.id)

        response = self.client.delete(f"{BASE_URL}/{order1.id}/items/{item2.id+1}")
        found = Items.find_by_order_id(order_id=order1.id)
        count = len([item for item in found])
        self.assertEqual(count, 1)

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

        # Check the data is correct
        new_order = response.get_json()
        self.assertEqual(new_order["user_id"], test_order.user_id)
        self.assertEqual(new_order["create_time"], test_order.create_time)
        self.assertEqual(new_order["status"], test_order.status)
    
    def test_add_order_item(self):
        """ It should add an item to the order"""
        order1 = Order(user_id=123, create_time="2021-10-10", status=1)
        order1.create()
        item1 = Items(order_id=order1.id, item_id= 1)
        item1.create()

        response = self.client.post(f"{BASE_URL}/{order1.id}/items", json=item1.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check the data
        new_item = response.get_json()
        self.assertIsNotNone(new_item)
        self.assertEqual(new_item["order_id"], item1.order_id)
        self.assertEqual(new_item["item_id"], item1.item_id)

        response = self.client.post(f"{BASE_URL}/{404}/items", json=item1.serialize())
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(""==response.get_json())

    def test_list_order(self):
        """ It should list existing orders """
        order1 = self._create_order_by_info(0, "2021-10-18", 1)
        order2 = self._create_order_by_info(0, "2021-10-17", 2)
        order3 = self._create_order_by_info(1, "2021-10-16", 1)

        resp = self.client.get(BASE_URL + "/orders", query_string="user_id=0")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertIsNone(data)
        self.assertEqual(len(data), 2)

    def test_list_order_items(self):
        """ It should list the items in an order"""            
        order = self._create_order_by_info(0, "2021-10-18", 1)
        item1 = self._create_item(order.id, 0)
        item2 = self._create_item(order.id, 1)

        resp = self.client.get(f"{BASE_URL}/orders/{order.id}/items")
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        data = resp.get_json()
        self.assertIsNone(data)
        self.assertEqual(len(data), 2)
