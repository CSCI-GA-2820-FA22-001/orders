"""
My Service

Describe what your service does here
"""
import logging
from flask import jsonify, request, url_for, make_response, abort
from .common import status  # HTTP Status Codes
from service.models import Order, Items, Status
# Import Flask application
from . import app

logger = logging.getLogger("flask.app")

############################################################
# Health Endpoint
############################################################


@app.route("/health")
def health():
	"""Health Status"""
	return jsonify(dict(status="OK")), status.HTTP_200_OK


######################################################################
# GET INDEX
######################################################################


@app.route("/", methods=["GET"])
def index():
	""" Root URL response """
	return app.send_static_file("index.html")


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
	json_data = request.get_json()
	app.logger.info("Request create an order")
	check_content_type("application/json")
	order = Order()
	order.deserialize(json_data)
	order.create()
	# return a message
	message = order.serialize()
	message["items"] = []

	if json_data is not None:
		if json_data.get("items") is not None and isinstance(json_data["items"], list):
			for item_id in json_data.get("items"):
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
		abort(status.HTTP_404_NOT_FOUND, f"Order with id '{order_id}' was not found.")

	order_data = order.serialize()
	order_data["items"] = []
	items = Items.find_by_order_id(order_id)
	for item in items:
		order_data["items"].append(item.item_id)

	app.logger.info("Returning pet: %s", order.id)
	# return jsonify(order_data), status.HTTP_200_OK
	return make_response(jsonify(order_data), status.HTTP_200_OK)


@app.route("/orders/<int:order_id>", methods=["PUT"])
def update_order(order_id):
	"""Update order by order id
	TODO: check if target id == json id
	Args:
		order_id (int): the id of the order
	"""
	order: Order = Order.find(order_id)
	if order:
		order.deserialize(request.get_json())
		order.update()
		return make_response("", status.HTTP_200_OK)
	else:
		return make_response("", status.HTTP_404_NOT_FOUND)


@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
	"""
	Delete order by order id
	Args:
		order_id (int): the id of the order
	"""
	order = Order.find(order_id)
	if order:
		order.delete()
	return make_response("", status.HTTP_204_NO_CONTENT)


@app.route("/orders/<int:order_id>/cancel", methods=["POST"])
def cancel_order(order_id):
	"""Cancel an order
	Args:
		order_id (int): the id of the order
	"""
	order = Order.find(order_id)
	if order:
		order.status = Status.CANCELLED
		order.update()
		return make_response("", status.HTTP_200_OK)
	else:
		return make_response("", status.HTTP_404_NOT_FOUND)


@app.route("/orders/<int:order_id>/items", methods=["GET"])
def list_order_items(order_id):
	"""List order items by order id
	Args:
		order_id (int): the unique id representing an order
	Returns:
		list[items]: a list of items in that order
	"""

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
		return make_response(jsonify(message), status.HTTP_201_CREATED)
	else:
		message = "order not found"
		return make_response(jsonify(message), status.HTTP_404_NOT_FOUND)


@app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["GET"])
def get_order_item(order_id, item_id):
	"""Get items in order

	Args:
		order_id (int): the id of the order
		item_id (int): the id of the order
	"""
	order = Order.find(order_id)
	if order:
		items = Items.find_by_order_id(order_id)
		for item in items:
			if item.item_id == item_id:
				return make_response("item exist in order", status.HTTP_200_OK)
		return make_response("item not exist in order", status.HTTP_204_NO_CONTENT)
	else:
		return make_response("", status.HTTP_204_NO_CONTENT)


@app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["PUT"])
def update_order_item(order_id, item_id):
	"""Update items in order

	Args:
		order_id (int): the id of the order
		item_id (int): the id of the order
	"""
	order: Order = Order.find(order_id)
	if order:
		items = Items.find_by_order_id(order_id)
		for item in items:
			if item.item_id == item_id:
				item.deserialize(request.get_json())
				item.update()
				return make_response("", status.HTTP_200_OK)
		return make_response("", status.HTTP_204_NO_CONTENT)
	else:
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


@app.route("/orders/user/<int:id>/status/<int:st>", methods=["GET"])
def get_order_by_status(id, st):
	if st not in [int(Status.CREATED), int(Status.COMPLETED), int(Status.CANCELLED)]:
		return make_response(jsonify(f"Invalid Status {st}"), status.HTTP_400_BAD_REQUEST)
	orders = Order.find_by_status(id, st)
	if orders.count():
		order_list = [order.serialize() for order in orders]
		return make_response(jsonify(order_list), status.HTTP_200_OK)
	else:
		return make_response("", status.HTTP_204_NO_CONTENT)


@app.route("/orders/items/<int:item_id>", methods=["GET"])
def get_order_by_item(item_id):
	orders = Items.find_by_item_id(item_id)
	if orders.count():
		order_list = [order.serialize() for order in orders]
		return make_response(jsonify(order_list), status.HTTP_200_OK)
	else:
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
