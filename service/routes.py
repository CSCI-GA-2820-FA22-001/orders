"""
My Service

Describe what your service does here
"""
from crypt import methods
from email.policy import HTTP
import logging
from flask import Flask, jsonify, request, url_for, make_response, abort
from .common import status  # HTTP Status Codes
from service.models import Order

# Import Flask application
from . import app
logger = logging.getLogger("flask.app")

######################################################################
# GET INDEX
######################################################################
@app.route("/")
def index():
    """ Root URL response """
    return (
        "Reminder: return some useful information in json format about the service here",
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
    print(order.items)
    order.create()
    # return a message
    message = order.serialize()
    location_url = url_for("create_order", order_id=order.id, _external=True)
    return make_response(
        jsonify(message), status.HTTP_201_CREATED, {"Location": location_url}
    )

@app.route("/orders/<int:order_id>", methods=["DELETE"])
def delete_order(order_id):
    """Delete order by order id

    Args:
        order_id (int): the id of the order
    """
    order = Order.find(order_id)
    print(order)
    if order:
        order.delete()
    return make_response("", status.HTTP_204_NO_CONTENT)

@app.route("/orders/test", methods=["GET"])
def test_db():
    od = Order.all()
    location_url = url_for("test_db", order_id=1, _external=True)
    print(location_url)
    return make_response(
        jsonify({"st": "succ"}), status.HTTP_201_CREATED, {"Location": location_url}
    )

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