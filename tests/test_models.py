"""
Test cases for YourResourceModel Model

"""
import os
import logging
import unittest

from importlib_metadata import metadata
from service import app
from service.models import Order, DataValidationError, db
from service.config import DATABASE_URI


######################################################################
#  <your resource name>   M O D E L   T E S T   C A S E S
######################################################################
class TestOrderModel(unittest.TestCase):
    """ Test Cases for YourResourceModel Model """

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
        order = Order(user_id=123, create_time="2022-10-16", status=1)
        order.create()
        self.assertEqual(str(order), "<User 123 Create Time=2022-10-16 Status=1>")
        self.assertTrue(order is not None)
        self.assertEqual(order.user_id, 123)
        self.assertEqual(order.create_time, "2022-10-16")
        self.assertEqual(order.status, 1)
        
    def test_delete_order(self):
        order = Order(user_id=123, create_time="2022-10-16", status=1)
        order.create()
        order_id = order.id
        order.delete()
        o = Order.find(order_id)
        self.assertEqual(o, None)

