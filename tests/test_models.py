"""
Test cases for YourResourceModel Model

"""
import os
import logging
import unittest
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

    @classmethod
    def tearDownClass(cls):
        """ This runs once after the entire test suite """
        db.session.close()

    def setUp(self):
        """ This runs before each test """
        pass

    def tearDown(self):
        """ This runs after each test """
        db.session.remove()

    ######################################################################
    #  T E S T   C A S E S
    ######################################################################

    def test_create_order(self):
        """ It should always be true """
        orders = Order.all()

