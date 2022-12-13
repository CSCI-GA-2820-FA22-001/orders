"""
My Service

Describe what your service does here
"""
import logging
import secrets
from flask import jsonify, request, make_response, abort
from flask_restx import Api, Resource, fields, reqparse
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


######################################################################
# Configure Swagger before initializing it
######################################################################


api = Api(
	app,
	version='1.0.0',
	title='orders REST API Service',
	description='This is a server for orders.',
	default='orders',
	default_label='orders operations',
	doc='/apidocs',  # default also could use doc='/apidocs/'
)


######################################################################
# Function to generate a random API key (good for testing)
######################################################################
def generate_apikey():
	""" Helper function used when testing API keys """
	return secrets.token_hex(16)


create_model = api.model('Order', {
	'user_id': fields.Integer(description='The user id of the order', required=False),
	'status': fields.String(enum=Status._member_names_, description='The status of the order', required=False),
	'create_time': fields.Integer(description='The create time of the order', required=False),
})

order_model = api.inherit(
	'OrderModel',
	create_model,
	{
		'id': fields.Integer(
			readOnly=True,
			description='The unique id assigned internally by service')
	}
)

order_args = reqparse.RequestParser()
order_args.add_argument(
	'user_id', type=int, location='args',
	required=False, help='List Orders by user_id')
order_args.add_argument(
	'status', type=int, location='args',
	required=False, help='List Orders by status')
order_args.add_argument(
	'create_time', type=int,
	location='args', required=False, help='List Orders by create_time')
order_args.add_argument(
	'item_id', type=int,
	location='args', required=False, help='List Orders by item_id')
order_args.add_argument(
	'items', type=list,
	location='args', required=False, help='Create Order with items')


@api.route("/orders")
class OrderResource(Resource):
	"""OrderResource class
	"""
	@api.doc('search_order')
	@api.response(401, 'Unauthorized user for unknown user_id')
	@api.response(400, 'Invalid data')
	@api.response(204, 'Orders not found')
	def get(self):
		"""List all orders

		Keyword arguments:
		user_id -- the unique id representing a user (required)
		status -- the status to filter the orders (optional)
		item_id -- item id to filter the orders (optional)
		Return: all related orders owned by user with user_id
		"""
		app.logger.info("Request listing orders")
		args = order_args.parse_args()
		user_id = args["user_id"]
		if user_id is None:
			abort(
				status.HTTP_401_UNAUTHORIZED,
				description="Unauthorized user for unknown user_id.",
			)

		st = args["status"]
		if st is not None:
			if st != Status.CREATED.value and \
				st != Status.COMPLETED.value and \
				st != Status.CANCELLED.value:
				return f"Invalid Status {st}", status.HTTP_400_BAD_REQUEST

			orders = Order.find_by_status(user_id, st)
			if orders.count():
				order_list = [order.serialize() for order in orders]
				return order_list, status.HTTP_200_OK
			else:
				return "", status.HTTP_204_NO_CONTENT

		item_id = args["item_id"]
		if item_id is not None:
			items = Items.find_by_item_id(item_id)
			if items.count():
				orders = []
				for item in items:
					order = Order.find(by_id=item.order_id)
					orders.append(order.serialize())
				return orders, status.HTTP_200_OK
			else:
				return "", status.HTTP_204_NO_CONTENT

		orders = Order.find_by_user_id(user_id)
		return [order.serialize() for order in orders], status.HTTP_200_OK

	@api.doc('create_order')
	@api.response(201, 'Order created')
	def post(self):
		"""Create an order
		request body: {
				"item": [id1, id2, ...]
		}
		"""
		json_data = api.payload
		app.logger.info("Request create an order")
		# check_content_type("application/json")
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

		location_url = api.url_for(
			OrderSingleResource, order_id=order.id, _external=True)
		return message, status.HTTP_201_CREATED, {"Location": location_url}


# @app.route("/orders", methods=["GET"])
# def list_orders():
#     """List all orders

#     Keyword arguments:
#     user_id -- the unique id representing a user (required)
#     status -- the status to filter the orders (optional)
#     item_id -- item id to filter the orders (optional)
#     Return: all related orders owned by user with user_id
#     """

#     app.logger.info("Request listing orders")
#     args = request.args
#     user_id = args.get("user_id", type=int)
#     if user_id is None:
#         abort(
#             status.HTTP_401_UNAUTHORIZED,
#             "Unauthorized user for unknown user_id.",
#         )

#     st = args.get("status", type=int)
#     if st is not None:
#         if st != Status.CREATED.value and \
#                 st != Status.COMPLETED.value and \
#                 st != Status.CANCELLED.value:
#             return make_response(jsonify(f"Invalid Status {st}"), status.HTTP_400_BAD_REQUEST)

#         orders = Order.find_by_status(user_id, st)
#         if orders.count():
#             order_list = [order.serialize() for order in orders]
#             return make_response(jsonify(order_list), status.HTTP_200_OK)
#         else:
#             return make_response("", status.HTTP_204_NO_CONTENT)

#     item_id = args.get("item_id", type=int)
#     if item_id is not None:
#         items = Items.find_by_item_id(item_id)
#         if items.count():
#             orders = []
#             for item in items:
#                 order = Order.find(by_id=item.order_id)
#                 orders.append(order.serialize())
#             return make_response(jsonify(orders), status.HTTP_200_OK)
#         else:
#             return make_response("", status.HTTP_204_NO_CONTENT)

#     orders = Order.find_by_user_id(user_id)
#     return make_response(
#         jsonify([order.serialize() for order in orders]),
#         status.HTTP_200_OK,
#     )


# @app.route("/orders", methods=["POST"])
# def create_order():
#     """Create an order
#     request body: {
#             "item": [id1, id2, ...]
#     }
#     """
#     json_data = request.get_json()
#     app.logger.info("Request create an order")
#     check_content_type("application/json")
#     order = Order()
#     order.deserialize(json_data)
#     order.create()
#     # return a message
#     message = order.serialize()
#     message["items"] = []

#     if json_data is not None:
#         if json_data.get("items") is not None and isinstance(json_data["items"], list):
#             for item_id in json_data.get("items"):
#                 items = Items()
#                 items.order_id = order.id
#                 items.item_id = item_id
#                 items.create()
#                 message["items"].append(item_id)

#     location_url = url_for("create_order", order_id=order.id, _external=True)
#     return make_response(
#         jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
#     )

@api.route("/orders/all")
class AllOrderResource(Resource):
	"""AllOrderResource class
	"""
	@api.doc('get_all_orders')
	@api.marshal_list_with(order_model)
	def get(self):
		"""List all orders
		"""
		app.logger.info("List all order in the database")
		orders = Order.all()
		return [order.serialize() for order in orders], status.HTTP_200_OK


# @app.route("/orders/all", methods=["GET"])
# def get_all_order():
#     app.logger.info("List all order in the database")
#     orders = Order.all()
#     return make_response(
#         jsonify([order.serialize() for order in orders]),
#         status.HTTP_200_OK,
#     )


@api.route("/orders/<int:order_id>")
@api.param('order_id', 'The order identifier')
class OrderSingleResource(Resource):
	"""OrderSingleResource
	"""
	@api.doc('get_order_by_id')
	@api.response(404, 'Order not found')
	def get(self, order_id):
		"""Get order by order id
		Args:
				order_id (int): the id of the order
		"""
		app.logger.info("Request for pet with id: %s", order_id)
		order = Order.find(order_id)
		if not order:
			abort(
				status.HTTP_404_NOT_FOUND,
				f"Order with id '{order_id}' was not found.")

		order_data = order.serialize()
		order_data["items"] = []
		items = Items.find_by_order_id(order_id)
		for item in items:
			order_data["items"].append(item.item_id)

		app.logger.info("Returning pet: %s", order.id)
		# return jsonify(order_data), status.HTTP_200_OK
		return order_data, status.HTTP_200_OK

	@api.doc('put_order_by_id')
	@api.response(200, 'Success')
	@api.response(404, 'Order not found')
	def put(self, order_id):
		"""Update order by order id
		TODO: check if target id == json id
		Args:
				order_id (int): the id of the order
		"""
		order: Order = Order.find(order_id)
		if order:
			order.deserialize(api.payload)
			order.update()
			return "", status.HTTP_200_OK
		else:
			return "", status.HTTP_404_NOT_FOUND

	@api.doc('delete_order_by_id')
	@api.response(204, 'Order deleted')
	def delete(self, order_id):
		"""
		Delete order by order id
		Args:
				order_id (int): the id of the order
		"""
		order = Order.find(order_id)
		if order:
			order.delete()
		return "", status.HTTP_204_NO_CONTENT


# @app.route("/orders/<int:order_id>", methods=["GET"])
# def get_order_by_id(order_id):
#     """Get order by order id

#     Args:
#             order_id (int): the id of the order
#     """
#     app.logger.info("Request for pet with id: %s", order_id)
#     order = Order.find(order_id)
#     if not order:
#         abort(status.HTTP_404_NOT_FOUND,
#               f"Order with id '{order_id}' was not found.")

#     order_data = order.serialize()
#     order_data["items"] = []
#     items = Items.find_by_order_id(order_id)
#     for item in items:
#         order_data["items"].append(item.item_id)

#     app.logger.info("Returning pet: %s", order.id)
#     # return jsonify(order_data), status.HTTP_200_OK
#     return make_response(jsonify(order_data), status.HTTP_200_OK)


# @app.route("/orders/<int:order_id>", methods=["PUT"])
# def update_order(order_id):
#     """Update order by order id
#     TODO: check if target id == json id
#     Args:
#             order_id (int): the id of the order
#     """
#     order: Order = Order.find(order_id)
#     if order:
#         order.deserialize(request.get_json())
#         order.update()
#         return make_response("", status.HTTP_200_OK)
#     else:
#         return make_response("", status.HTTP_404_NOT_FOUND)


# @app.route("/orders/<int:order_id>", methods=["DELETE"])
# def delete_order(order_id):
#     """
#     Delete order by order id
#     Args:
#             order_id (int): the id of the order
#     """
#     order = Order.find(order_id)
#     if order:
#         order.delete()
#     return make_response("", status.HTTP_204_NO_CONTENT)

@api.route("/orders/<int:order_id>/cancel")
@api.param('order_id', 'The order identifier')
class CancelOrderResource(Resource):
	"""CancelOrderResource class
	"""
	@api.doc('cancel_order_by_id')
	@api.response(404, 'Order not found')
	def post(self, order_id):
		"""Cancel an order
		Args:
				order_id (int): the id of the order
		"""
		order = Order.find(order_id)
		if order:
			order.status = Status.CANCELLED
			order.update()
			return "", status.HTTP_200_OK
		else:
			return "", status.HTTP_404_NOT_FOUND

# @app.route("/orders/<int:order_id>/cancel", methods=["POST"])
# def cancel_order(order_id):
#     """Cancel an order
#     Args:
#             order_id (int): the id of the order
#     """
#     order = Order.find(order_id)
#     if order:
#         order.status = Status.CANCELLED
#         order.update()
#         return make_response("", status.HTTP_200_OK)
#     else:
#         return make_response("", status.HTTP_404_NOT_FOUND)


@api.route("/orders/<int:order_id>/items")
@api.param('order_id', 'The order identifier')
class ItemResource(Resource):
	"""ItemResource
	"""
	@api.doc('list_item_of_order')
	def get(self, order_id):
		"""List order items by order id
		Args:
				order_id (int): the unique id representing an order
		Returns:
				list[items]: a list of items in that order
		"""
		items = Items.find_by_order_id(order_id)
		return [item.serialize() for item in items], status.HTTP_200_OK

	@api.doc('add_item_to_order')
	@api.response(404, 'Order not found')
	@api.response(201, 'Item added')
	def post(self, order_id):
		"""Add item to order by id

		Keyword arguments:
				order_id -- the id of the order
		"""
		app.logger.info("Request add an item to order: %s", order_id)
		check_content_type("application/json")
		order = Order.find(order_id)
		if order:
			item = Items()
			item.deserialize(api.payload)
			item.create()
			# return a message
			message = item.serialize()
			return message, status.HTTP_201_CREATED
		else:
			message = "order not found"
			return message, status.HTTP_404_NOT_FOUND


# @app.route("/orders/<int:order_id>/items", methods=["GET"])
# def list_order_items(order_id):
#     """List order items by order id
#     Args:
#             order_id (int): the unique id representing an order
#     Returns:
#             list[items]: a list of items in that order
#     """

#     items = Items.find_by_order_id(order_id)
#     return make_response(jsonify([item.serialize() for item in items]), status.HTTP_200_OK)


# @app.route("/orders/<int:order_id>/items", methods=["POST"])
# def add_order_item(order_id):
#     """Add item to order by id

#     Keyword arguments:
#             order_id -- the id of the order
#     """
#     app.logger.info("Request add an item to order: %s", order_id)
#     check_content_type("application/json")
#     order = Order.find(order_id)
#     if order:
#         item = Items()
#         item.deserialize(request.get_json())
#         item.create()
#         # return a message
#         message = item.serialize()
#         return make_response(jsonify(message), status.HTTP_201_CREATED)
#     else:
#         message = "order not found"
#         return make_response(jsonify(message), status.HTTP_404_NOT_FOUND)

@api.route("/orders/<int:order_id>/items/<int:item_id>")
@api.param('order_id', 'The order identifier')
@api.param('item_id', 'The item identifier')
class SingleItemResource(Resource):
	"""SingleItemResource
	"""
	@api.doc('get_item_in_order')
	@api.response(204, 'Order or item not found')
	def get(self, order_id, item_id):
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
					return "item exist in order", status.HTTP_200_OK
			return "item not exist in order", status.HTTP_204_NO_CONTENT
		else:
			return "", status.HTTP_204_NO_CONTENT

	@api.doc('update_item_in_order')
	@api.response(200, "Success")
	@api.response(204, 'Order or item not found')
	def put(self, order_id, item_id):
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
					item.deserialize(api.payload)
					item.update()
					return make_response("", status.HTTP_200_OK)
			return "", status.HTTP_204_NO_CONTENT
		else:
			return "", status.HTTP_204_NO_CONTENT

	@api.doc('delete_item_in_order')
	@api.response(204, 'Item deleted')
	def delete(self, order_id, item_id):
		"""Delete items in order

		Args:
				order_id (int): the id of the order
				item_id (int): the id of the order
		"""
		order = Order.find(order_id)
		if order:
			app.logger.info("Calling delete item on order %s", order.id)
			found = Items.find_by_order_id(order_id)
			for item in found:
				app.logger.info("try match with item = %s target = %s", item.id, item_id)
				if item.item_id == item_id:
					item.delete()
					app.logger.info("Target Found, deleted item %s", item.id)
			
		app.logger.info("Calling delete item finished")
		return "", status.HTTP_204_NO_CONTENT


# @app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["GET"])
# def get_order_item(order_id, item_id):
#     """Get items in order

#     Args:
#             order_id (int): the id of the order
#             item_id (int): the id of the order
#     """
#     order = Order.find(order_id)
#     if order:
#         items = Items.find_by_order_id(order_id)
#         for item in items:
#             if item.item_id == item_id:
#                 return make_response("item exist in order", status.HTTP_200_OK)
#         return make_response("item not exist in order", status.HTTP_204_NO_CONTENT)
#     else:
#         return make_response("", status.HTTP_204_NO_CONTENT)


# @app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["PUT"])
# def update_order_item(order_id, item_id):
#     """Update items in order

#     Args:
#             order_id (int): the id of the order
#             item_id (int): the id of the order
#     """
#     order: Order = Order.find(order_id)
#     if order:
#         items = Items.find_by_order_id(order_id)
#         for item in items:
#             if item.item_id == item_id:
#                 item.deserialize(request.get_json())
#                 item.update()
#                 return make_response("", status.HTTP_200_OK)
#         return make_response("", status.HTTP_204_NO_CONTENT)
#     else:
#         return make_response("", status.HTTP_204_NO_CONTENT)


# @app.route("/orders/<int:order_id>/items/<int:item_id>", methods=["DELETE"])
# def delete_order_item(order_id, item_id):
#     order = Order.find(order_id)
#     if order:
#         found = Items.find_by_order_id(order_id)
#         for item in found:
#             if item.id == item_id:
#                 item.delete()
#     return make_response("", status.HTTP_204_NO_CONTENT)


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
