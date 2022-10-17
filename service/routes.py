"""
My Service

Describe what your service does here
"""
from ast import arg
from crypt import methods
from email.policy import HTTP
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from .common import status  # HTTP Status Codes
from service.models import Items, Order

# Import Flask application
from . import app
import json
logger = logging.getLogger("flask.app")

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        jsonify(
            name="Order REST API Service",
            version="1.0",
            paths=url_for("/", _external=True),
        ),
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
    location_url = url_for("create_order", order_id=order.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
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
            "unauthorized user",
        )
    
    orders = Order.find_by_user_id(user_id)
    return make_response(
        jsonify(order.serialize() for order in orders), 
        status.HTTP_200_OK,
    )


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
    return make_response(jsonify(item.serialize() for item in items), status.HTTP_200_OK)



@app.route("/orders/<int:order_id>/items/<int:item_id>")
def delete_order_item(order_id, item_id):
    order = Order.find(order_id)
    if order:
        items = json.loads(order.items)
        if item_id in items:
            items.remove(item_id)
            order.items = json.dumps(items)
            order.update()
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