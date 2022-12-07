import requests
from behave import given
from compare import expect


@given('the following orders')
def step_impl(context):
	""" Delete all Pets and load new ones """
	# List all of the pets and delete them one by one
	rest_endpoint = f"{context.BASE_URL}/orders"
	context.resp = requests.get(rest_endpoint, params={"user_id": 1})
	expect(context.resp.status_code).to_equal(200)
	for order in context.resp.json():
		context.resp = requests.delete(f"{rest_endpoint}/{order['id']}")
		expect(context.resp.status_code).to_equal(204)

	# load the database with new pets
	# TODO
