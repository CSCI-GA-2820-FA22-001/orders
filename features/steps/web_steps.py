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


@when('I press "{button_id}" button')
def step_impl(context, button_id):
	context.driver.find_element_by_id(button_id).click()

@when('I set the "{element_id}" to "{text_string}"')
def step_impl(context, element_id, text_string):
	element = context.driver.find_element_by_id(element_id)
	element.clear()
	element.send_keys(text_string)

@then('I should see "{text}" in the "{element_id}"')
def step_impl(context, text, element_id):
	element = context.driver.find_element_by_id(element_id)
	expect(element.text).to_equal(text)
