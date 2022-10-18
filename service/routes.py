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
	
	for item_id in request.get_json().get("items",[]):
		items = Items()
		items.order_id = order.id
		items.item_id = item_id
		items.create()
		# return a message
		message_item = items.serialize()


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