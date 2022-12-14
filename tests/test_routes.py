"""
TestYourResourceModel API Service Test Suite

Test cases can be run with the following:
nosetests -v --with-spec --spec-color
coverage report -m
"""
import os
import logging
from unittest import TestCase

from flask import jsonify
from service import app, error_handlers
from service.models import db, Order, Items, Status
from service.common import status  # HTTP Status Codes
from time import time

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
		db.session.query(Items).delete()
		db.session.commit()

	def tearDown(self):
		""" This runs after each test """
		db.session.remove()

	######################################################################
	#  H E L P E R S   F U N C T I O N S   H E R E
	######################################################################

	def _create_order(self, count, user_id_begin=0, user_id_incr=0):
		"""Factory method to create orders in bulk
		param:
			count -> int: represent how many orders you want to generate
			user_id_incr -> int: what is the difference between previous user id and next user id
		"""
		orders = []
		user_id = user_id_begin
		for _ in range(count):
			order = Order(user_id=user_id, create_time=(int)(time()), status=Status.CREATED)
			orders.append(order)
			user_id += user_id_incr
		return orders

	######################################################################
	#  P L A C E   T E S T   C A S E S   H E R E
	######################################################################

	def test_index(self):
		""" It should call the home page """
		resp = self.client.get("/")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

	def test_update_order(self):
		""" test update /orders/<int:order_id>"""
		order = self._create_order(count=1, user_id_incr=1)[0]
		order.create()

		# update
		updated_order = self._create_order(count=1, user_id_incr=1)[0]
		updated_order.status = Status.CREATED

		db_order = Order.find(order.id)
		self.assertEqual(db_order.status, Status.CREATED)
		response = self.client.put(f"{BASE_URL}/{order.id}", json=updated_order.serialize())
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		db_order = Order.find(order.id)
		self.assertEqual(db_order.status, Status.CREATED)

		# update an order that is not in database
		not_in_db_order = self._create_order(count=1, user_id_begin=100000001)[0]
		not_in_db_order.id = 100000001

		response = self.client.put(f"{BASE_URL}/{not_in_db_order.id}", json=not_in_db_order.serialize())
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

	def test_update_order_item(self):
		""" test update /orders/<int:order_id>/items/<int:item_id>"""
		# orders = self._create_order(count=1, user_id_incr=0)[0]
		org_order = self._create_order(count=1, user_id_incr=0)[0]
		altered_order = self._create_order(count=1, user_id_incr=0)[0]
		org_order.create()
		altered_order.create()

		item1 = Items(order_id=org_order.id, item_id=1)
		item1.create()

		# upadte item
		updated_item1 = Items(order_id=altered_order.id, item_id=1)

		response = self.client.put(f"{BASE_URL}/10000000/items/{item1.item_id}", json=updated_item1.serialize())
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		response = self.client.put(f"{BASE_URL}/{org_order.id}/items/1000000", json=updated_item1.serialize())
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		response = self.client.put(f"{BASE_URL}/{org_order.id}/items/{item1.item_id}", json=updated_item1.serialize())
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		# not exist in original order
		db_items = Items.find_by_order_id(org_order.id)
		id_list = [it.item_id for it in db_items]
		self.assertFalse(item1.item_id in id_list)

		# exist in new order
		db_items = Items.find_by_order_id(altered_order.id)
		id_list = [it.item_id for it in db_items]
		self.assertTrue(item1.item_id in id_list)

	def test_get_order_item(self):
		""" test update /orders/<int:order_id>/items/<int:item_id>"""
		orders = self._create_order(2, 0)
		org_order = orders[0]
		altered_order = orders[1]
		org_order.create()
		altered_order.create()

		item1 = Items(order_id=org_order.id, item_id=1)
		item1.create()

		response = self.client.get(f"{BASE_URL}/{org_order.id}/items/{item1.item_id}", json=item1.serialize())
		self.assertEqual(response.status_code, status.HTTP_200_OK)

		response = self.client.get(f"{BASE_URL}/{org_order.id}/items/10000", json=item1.serialize())
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		response = self.client.get(f"{BASE_URL}/100000/items/{item1.item_id}", json=item1.serialize())
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		response = self.client.get(f"{BASE_URL}/20/items/{item1.item_id}", json=item1.serialize())
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

	def test_delete_order(self):
		""" test Delete /orders/<int:order_id>"""
		order = self._create_order(count=1, user_id_incr=1)[0]
		order.create()
		response = self.client.delete(f"{BASE_URL}/{order.id}")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
		db_order = Order.find(order.id)
		self.assertEqual(db_order, None)
		# Todo: get this item and check if it's none

	def test_delete_item(self):
		""" test delete item by order id and item id"""
		order1 = Order(user_id=123, create_time=(int)(time()), status=Status.CREATED)
		order1.create()
		item1 = Items(order_id=order1.id, item_id=1)
		item2 = Items(order_id=order1.id, item_id=2)
		item1.create()
		item2.create()
		response = self.client.delete(f"{BASE_URL}/{order1.id}/items/{item1.item_id}")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		found = Items.find_by_order_id(order_id=order1.id)
		count = len([item for item in found])
		self.assertEqual(count, 1)
		self.assertEqual(found[0].item_id, item2.item_id)

		response = self.client.delete(f"{BASE_URL}/{order1.id}/items/{item2.item_id+1}")
		found = Items.find_by_order_id(order_id=order1.id)
		count = len([item for item in found])
		self.assertEqual(count, 1)

	def test_get_order(self):
		""" It should Get the Order with the order_id"""
		info_item = {
			"user_id": 0,
			"create_time": (int)(time()),
			"status": Status.CREATED,
			"items": [1,2,3]
		}

		response = self.client.post(BASE_URL, json=info_item)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		test_id = response.get_json().get("id")
		response = self.client.get(f"{BASE_URL}/{test_id}")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		new_order = response.get_json()
		self.assertEqual(new_order["user_id"], info_item["user_id"])
		self.assertEqual(new_order["create_time"], info_item["create_time"])
		self.assertEqual(new_order["status"], info_item["status"])
		self.assertEqual(new_order.get("items"), info_item["items"])

		response = self.client.get(f"{BASE_URL}/10000")
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

		order = Order(user_id=1, create_time=int(123456), status=Status.CREATED)
		order.create()
		item = Items(order_id=order.id, item_id=22)
		item.create()
		response = self.client.get(f"{BASE_URL}?user_id=1&item_id={item.item_id}")
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_order(self):
		""" It should Create a new Order"""
		info_item = {
			"user_id": 0,
			"create_time": (int)(time()),
			"status": Status.CREATED,
			"items": [1,2,3]
		}
		test_order = Order()
		test_order = test_order.deserialize(info_item)
		test_order.create()

		logging.debug("Test Order: %s", test_order.serialize())
		response = self.client.post(BASE_URL, json=info_item)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		# Check the data is correct
		new_order = response.get_json()
		self.assertEqual(new_order["user_id"], test_order.user_id)
		self.assertEqual(new_order["create_time"], test_order.create_time)
		self.assertEqual(new_order["status"], test_order.status)

		# Test for loop Items create

		for item_id in jsonify(info_item).get_json().get("items"):
			items = Items()
			items.order_id = test_order.id
			items.item_id = item_id
			items.create()
		found = Items.find_by_order_id(test_order.id)
		item_list = [item for item in found]
		count = len(item_list)
		self.assertEqual(count, 3)
		self.assertEqual(found[2].order_id, test_order.id)
		self.assertEqual(found[2].item_id, 3)

	def test_add_order_item(self):
		""" It should add an item to the order"""
		order1 = Order(user_id=123, create_time=(int)(time()), status=Status.CREATED)
		order1.create()
		item1 = Items(order_id=order1.id, item_id=1)
		item1.create()

		response = self.client.post(f"{BASE_URL}/{order1.id}/items", json=item1.serialize())
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

		# Check the data
		new_item = response.get_json()
		self.assertIsNotNone(new_item)
		self.assertEqual(new_item["order_id"], item1.order_id)
		self.assertEqual(new_item["item_id"], item1.item_id)

		response = self.client.post(f"{BASE_URL}/{404}/items", json=item1.serialize())
		self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
		self.assertTrue("order not found" == response.get_json())

	def test_list_orders(self):
		""" It should list existing orders """
		orders = self._create_order(count=2, user_id_begin=0, user_id_incr=0)
		order_excep = self._create_order(count=1, user_id_begin=1, user_id_incr=0)

		for order in orders:
			order.create()
		for order in order_excep:
			order.create()

		resp = self.client.get(BASE_URL)
		self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
		# data = resp.get_json()
		# self.assertIsNone(data)

		resp = self.client.get(BASE_URL, query_string="user_id=0")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		data = resp.get_json()
		self.assertIsNotNone(data)
		self.assertEqual(len(data), 2)

	def test_list_order_items(self):
		""" It should list the items in an order"""
		order = self._create_order(count=1, user_id_begin=0, user_id_incr=0)
		for o in order:
			o.create()
		item1 = Items(order_id=order[0].id, item_id=1)
		item1.create()
		item2 = Items(order_id=order[0].id, item_id=2)
		item2.create()

		resp = self.client.get(f"{BASE_URL}/{order[0].id}/items")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		data = resp.get_json()
		self.assertIsNotNone(data)
		self.assertEqual(len(data), 2)

	def test_cancel_order(self):
		""" It should cancel an order """
		order = self._create_order(count=1, user_id_begin=0, user_id_incr=0)[0]
		order.create()

		resp = self.client.get(f"{BASE_URL}/{order.id}")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		body = resp.get_json()
		self.assertIsNotNone(body)
		self.assertEqual(body["status"], Status.CREATED)

		resp = self.client.post(f"{BASE_URL}/{order.id}/cancel")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)

		resp = self.client.get(f"{BASE_URL}/{order.id}")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		body = resp.get_json()
		self.assertIsNotNone(body)
		self.assertEqual(body["status"], Status.CANCELLED)

		resp = self.client.post(f"{BASE_URL}/{order.id + 1}/cancel")
		self.assertEqual(resp.status_code, status.HTTP_404_NOT_FOUND)
		# body = resp.get_json()
		# self.assertIsNone(body)

	def test_get_order_by_status(self):
		"""test getting order by status"""
		ts = int(time())
		order1 = Order(user_id=1, create_time=ts, status=1)
		order2 = Order(user_id=1, create_time=ts, status=2)
		order3 = Order(user_id=1, create_time=ts, status=3)
		order4 = Order(user_id=1, create_time=ts + 1, status=1)
		order1.create()
		order2.create()
		order3.create()
		order4.create()
		resp = self.client.get(BASE_URL, query_string="user_id=1&status=1")
		self.assertEqual(resp.status_code, status.HTTP_200_OK)
		body = resp.get_json()
		res_order1 = Order().deserialize(body[0])
		res_order2 = Order().deserialize(body[1])
		self.assertEqual(res_order1.user_id, order1.user_id)
		self.assertEqual(res_order2.user_id, order4.user_id)
		self.assertEqual(res_order1.create_time, order1.create_time)
		self.assertEqual(res_order2.create_time, order4.create_time)
		self.assertEqual(res_order1.status, order1.status)
		self.assertEqual(res_order2.status, order4.status)
		resp = self.client.get(BASE_URL, query_string="status=4")
		self.assertEqual(resp.status_code, status.HTTP_401_UNAUTHORIZED)
		resp = self.client.get(BASE_URL, query_string="user_id=1&status=4")
		self.assertEqual(resp.status_code, status.HTTP_400_BAD_REQUEST)
		resp = self.client.get(BASE_URL, query_string="user_id=2&status=2")
		self.assertEqual(resp.status_code, status.HTTP_204_NO_CONTENT)

	def test_get_order_by_item_id(self):
		""" test getting order by item"""
		orders = self._create_order(count=3, user_id_begin=2, user_id_incr=0)
		order1 = orders[0]
		order2 = orders[1]
		order3 = orders[2]
		order1.create()
		order2.create()
		order3.create()

		item1 = Items(order_id=order1.id, item_id=1)
		item2 = Items(order_id=order2.id, item_id=1)
		item3 = Items(order_id=order3.id, item_id=1)
		item4 = Items(order_id=order1.id, item_id=2)
		item1.create()
		item2.create()
		item3.create()
		item4.create()

		response = self.client.get(BASE_URL, query_string="item_id=1")
		self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

		response = self.client.get(BASE_URL, query_string="user_id=2&item_id=3")
		self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

		response = self.client.get(BASE_URL, query_string="user_id=2&=item_id=1")
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		body = response.get_json()
		self.assertEqual(len(body), 3)
		self.assertEqual(body[0]["id"], item1.order_id)
		self.assertEqual(body[1]["id"], item2.order_id)
		self.assertEqual(body[2]["id"], item3.order_id)

	def test_route_health(self):
		"""test route health"""
		response = self.client.get("/health")
		body = response.get_json()
		self.assertEqual(response.status_code, status.HTTP_200_OK)
		self.assertEqual(body["status"], "OK")

	def test_request_validation_error(self):
		"""test_request_validation_error"""
		err_msg = "sample err message"
		result = error_handlers.request_validation_error(err_msg)
		self.assertEqual(str(result), str(error_handlers.bad_request(err_msg)))

	def test_resource_not_found(self):
		"""test_resource_not_found"""
		err_msg = "resource not found"
		result = error_handlers.not_found(err_msg)
		t = (
			jsonify(
				status=status.HTTP_404_NOT_FOUND,
				error="Not Found",
				message=err_msg,
			),
			status.HTTP_404_NOT_FOUND,
		)
		self.assertEqual(str(result), str(t))

	def test_method_not_supported(self):
		"""test_method_not_supported"""
		err_msg = "method: get_order"
		result = error_handlers.method_not_supported(err_msg)
		t = (
			jsonify(
				status=status.HTTP_405_METHOD_NOT_ALLOWED,
				error="Method not Allowed",
				message=err_msg,
			),
			status.HTTP_405_METHOD_NOT_ALLOWED,
		)
		self.assertEqual(str(result), str(t))

	def test_resource_conflict(self):
		"""test_resource_conflict"""
		err_msg = "resource conflict"
		result = error_handlers.resource_conflict(err_msg)
		t = (
			jsonify(
				status=status.HTTP_409_CONFLICT,
				error="Conflict",
				message=err_msg,
			),
			status.HTTP_409_CONFLICT,
		)
		self.assertEqual(str(result), str(t))

	def test_mediatype_not_supported(self):
		"""test_mediatype_not_supported"""
		err_msg = "media type not supported"
		result = error_handlers.mediatype_not_supported(err_msg)
		t = (
			jsonify(
				status=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
				error="Unsupported media type",
				message=err_msg,
			),
			status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
		)
		self.assertEqual(str(result), str(t))

	def test_internal_server_error(self):
		"""test_internal_server_error"""
		err_msg = "internal server error"
		result = error_handlers.internal_server_error(err_msg)
		t = (
			jsonify(
				status=status.HTTP_500_INTERNAL_SERVER_ERROR,
				error="Internal Server Error",
				message=err_msg,
			),
			status.HTTP_500_INTERNAL_SERVER_ERROR,
		)
		self.assertEqual(str(result), str(t))

	def test_get_all_order(self):
		"""test_get_all_order"""
		order1 = Order(user_id=123, create_time=(int)(time()), status=Status.CREATED)
		order1.create()
		order1 = Order(user_id=123, create_time=(int)(time()), status=Status.CREATED)
		order1.create()
		order1 = Order(user_id=123, create_time=(int)(time()), status=Status.CREATED)
		order1.create()
		result = self.client.get("/orders/all")
		body = result.get_json()
		self.assertEqual(result.status_code, status.HTTP_200_OK)
		self.assertEqual(len(body), 3)
