import logging
from behave import when, then
from compare import expect, ensure
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions


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


@then('I should see "{user_id}" in the result')
def step_impl(context, user_id):
	found = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
		expected_conditions.text_to_be_present_in_element(
			(By.ID, 'search_results'),
			user_id
		)
	)
	expect(found).to_be(True)


@when('I select "{text}" in the "{element_id}" dropdown')
def step_impl(context, text, element_id):
	element = Select(context.driver.find_element_by_id(element_id))
	element.select_by_visible_text(text)


@then('the "{element_id}" field should be empty')
def step_impl(context, element_id):
	element = context.driver.find_element_by_id(element_id)
	expect(element.get_attribute('value')).to_be(u'')

##################################################################
# These two function simulate copy and paste
##################################################################
@when('I copy the "{element_id}" field')
def step_impl(context, element_id):
	element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
		expected_conditions.presence_of_element_located((By.ID, element_id))
	)
	context.clipboard = element.get_attribute('value')
	logging.info('Clipboard contains: %s', context.clipboard)

@when('I paste the "{element_id}" field')
def step_impl(context, element_id):
	element = WebDriverWait(context.driver, context.WAIT_SECONDS).until(
		expected_conditions.presence_of_element_located((By.ID, element_id))
	)
	element.clear()
	element.send_keys(context.clipboard)


@then('I should not see "{name}" in the results')
def step_impl(context, name):
	element = context.driver.find_element_by_id('search_results')
	error_msg = "I should not see '%s' in '%s'" % (name, element.text)
	ensure(name in element.text, False, error_msg)

@then('I should see "{text}" in the "{element_id}" input value')
def step_impl(context, text, element_id):
	element = context.driver.find_element_by_id(element_id)
	error_msg = "I should see '%s' in '%s' not '%s'" % (text, element.text, element.get_attribute("value"))
	ensure(element.get_attribute("value") == text, True, error_msg)