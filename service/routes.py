"""
My Service

Describe what your service does here
"""
from crypt import methods
from email.policy import HTTP
import logging
from typing import List
from flask import Flask, jsonify, request, url_for, make_response, abort
from .common import status  # HTTP Status Codes
from service.models import Order, Items

# Import Flask application
from . import app
import json
logger = logging.getLogger("flask.app")

######################################################################
# GET INDEX
######################################################################
@app.route("/", methods=["GET"])
def index():
	""" Root URL response """
	return (
		"Home Page",
		status.HTTP_200_OK,
	)


@app.route("/orders", methods=["GET"])
def list_orders():
	"""List all orders
	
	Keyword arguments:
	user_id -- the unique id representing a user
	Return: all orders owned by user with user_id
	"""

	app.logger.info("Request listing orders")
	# TODO: how is parameter user_id passed?
	args = request.args
	user_id = args.get("user_id", type=int)
	if user_id is None:
		abort(
			status.HTTP_401_UNAUTHORIZED,
			"Unauthorized user for unknown user_id.",
		)
	
	orders = Order.find_by_user_id(user_id)
	return make_response(
		jsonify([order.serialize() for order in orders]), 
		status.HTTP_200_OK,
	)


@app.route("/orders", methods=["POST"])
def create_order():
	"""Create an order
	request body: {
		"item": [id1, id2, ...]
	}
	"""
	app.logger.info("Request create an order")
	check_content_type("application/json")
	order = Order()
	order.deserialize(request.get_json())
	order.create()
	# return a message
	message = order.serialize()
	message["items"] = []
	
	for item_id in request.get_json().get("items"):
		items = Items()
		items.order_id = order.id
		items.item_id = item_id
		items.create()
		message["items"].append(item_id)

	location_url = url_for("create_order", order_id=order.id, _external=True)
	return make_response(
		jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
	)


@app.route("/orders/<int:order_id>", methods=["GET"])
def get_order_by_id(order_id):
	"""Delete order by order id

	Args:
		order_id (int): the id of the order
	"""
	app.logger.info("Request for pet with id: %s", order_id)
	order = Order.find(order_id)
	if not order:
		abort(status.HTTP_404_NOT_FOUND, f"Pet with id '{order_id}' was not found.")
		
	app.logger.info("Returning pet: %s", order.id)
	return jsonify(order.serialize()), status.HTTP_200_OK


@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
	"""Update order by order id
	TODO: check if target id == json id
	Args:
		order_id (int): the id of the order
	"""
	order:Order = Order.find(order_id)
	if order:
		order.update()
		return make_response("", status.HTTP_200_OK)
	else:
		return make_response("", status.HTTP_204_NO_CONTENT)

@app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["PUT"])
def update_order_item(order_id, item_id):
	"""Update items in order

	Args:
		order_id (int): the id of the order
		item_id (int): the id of the order
	"""
	order:Order = Order.find(order_id)
	if order:
		items = Items.find_by_order_id(order_id)
		for item in items:
			if item.id == item_id:
				item.update()
		return make_response("", status.HTTP_200_OK)
	else:
		return make_response("", status.HTTP_204_NO_CONTENT)

@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
	"""Delete order by order id

	Args:
		order_id (int): the id of the order
	"""
	order = Order.find(order_id)
	if order:
		order.delete()
	return make_response("", status.HTTP_204_NO_CONTENT)


@app.route("/orders/<int:order_id>/items", methods=["GET"])
def list_order_items(order_id):
	"""List order items by order id
	Args:
		order_id (int): the unique id representing an order
	Returns:
		list[items]: a list of items in that order
	"""
	if order_id < 0:
		abort(
			status.HTTP_400_BAD_REQUEST,
			f"order id {order_id} should not be negative",
		)

	items = Items.find_by_order_id(order_id)
	return make_response(jsonify([item.serialize() for item in items]), status.HTTP_200_OK)


@app.route("/orders/<int:order_id>/items", methods=["POST"])
def add_order_item(order_id):
	"""Add item to order by id

	Keyword arguments:
		order_id -- the id of the order
	"""
	app.logger.info("Request add an item to order: %s", order_id)
	check_content_type("application/json")
	order = Order.find(order_id)
	if order:
		item = Items()
		item.deserialize(request.get_json())
		item.create()
		# return a message
		message = item.serialize()
	else:
		message = ""
	return make_response(jsonify(message),status.HTTP_201_CREATED)
	

@app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["DELETE"])
def delete_order_item(order_id, item_id):
	order = Order.find(order_id)
	if order:
		found = Items.find_by_order_id(order_id)
		for item in found:
			if item.id == item_id:
				item.delete()
	return make_response("", status.HTTP_204_NO_CONTENT)

######################################################################
#  U T I L I T Y   F U N C T I O N S
######################################################################


def init_db():
	""" Initializes the SQLAlchemy app """
	global app
	Order.init_db(app)

def check_content_type(media_type):
	""" Reference: https://github.com/nyu-devops/sample-accounts/blob/master/service/routes.py """
	"""Checks that the media type is correct"""
	content_type = request.headers.get("Content-Type")
	if content_type and content_type == media_type:
		return
	app.logger.error("Invalid Content-Type: %s", content_type)
	abort(
		status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
		f"Content-Type must be {media_type}",
	)