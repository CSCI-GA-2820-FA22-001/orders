from behave import when, then
from compare import expect
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import Select, WebDriverWait
# from selenium.webdriver.support import expected_conditions


@when('I visit the "home page"')
def step_impl(context):
	""" Make a call to the base URL """
	context.driver.get(context.BASE_URL)


@then('I should see "{message}" in the title')
def step_impl(context, message):
	""" Check the document title for a message """
	expect(context.driver.title).to_contain(message)
