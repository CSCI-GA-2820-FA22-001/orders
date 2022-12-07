import requests
from behave import given
from compare import expect
from service.models import Status


@given('the following orders')
def step_impl(context):
	""" Delete all Pets and load new ones """
	# List all of the pets and delete them one by one
	rest_endpoint = f"{context.BASE_URL}/orders/all"
	context.resp = requests.get(rest_endpoint)
	expect(context.resp.status_code).to_equal(200)
	for order in context.resp.json():
		context.resp = requests.delete(f"{context.BASE_URL}/orders/{order['id']}")
		expect(context.resp.status_code).to_equal(204)

	# load the database with new pets
	for row in context.table:
		# print(row)
		payload = {
			"user_id": int(row["user_id"]),
			"create_time": int(row["create_time"]),
			"status": int(row["status"]),
			"items": [int(x) for x in row["items"].split(",")]
		}
		context.resp = requests.post(f"{context.BASE_URL}/orders", json=payload)
		expect(context.resp.status_code).to_equal(201)
