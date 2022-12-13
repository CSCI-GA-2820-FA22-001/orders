Feature: The pet store service back-end
    As a User of Order syste
    I need a RESTful catalog service
    So that I can keep track of all my orders and items

Background:
    Given the following orders
        | user_id | create_time | status | items |
        | 1       | 1670369200  | 1      | 1,2   |
        | 1       | 1670369201  | 1      | 3,4   |
        | 1       | 1670369202  | 1      | 5     |
        | 1       | 1670369203  | 1      | 6     |
        | 23      | 1670461870  | 1      | 7     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order Demo RESTful Service" in the title

Scenario: List orders of a user
    When I visit the "Home Page"
    And I set the "user_id" to "1"
    And I press "list-order-btn" button
    Then I should see "Success" in the "flash_message"
    And I should see "1" in the result
    And I should see "1670369200" in the result
    And I should see "1670369201" in the result
    And I should see "1670369202" in the result
    And I should see "1670369203" in the result

Scenario: Create an order
    When I visit the "home page"
    And I set the "user_id" to "2"
    And I set the "items" to "1"
    And I select "Created" in the "status" dropdown
    And I press "create-order-btn" button
    # Then I should see "Success" in the "flash_message"
    When I set the "user_id" to "2"
    And I press "list-order-btn" button
    Then I should see "2" in the result

Scenario: Retrive an order
    When I visit the "home page"
    And I set the "user_id" to "1"
    And I press "list-order-btn" button
    And I copy the "order_id" field
    And I press "clear-order-btn" button
    And I paste the "order_id" field
    And I press "retrieve-order-btn" button
    Then I should see "1670369200" in the "create_time" input value
    And I should see "1" in the "user_id" input value
    And I should see "Created" in the "status" input value

Scenario: Update an order
    When I visit the "home page"
    And I set the "user_id" to "1"
    And I press "list-order-btn" button
    And I set the "user_id" to "2"
    And I set the "items" to "9,10"
    And I select "Completed" in the "status" dropdown
    And I press "update-order-btn" button
    And I press "clear-order-btn" button
    And I set the "user_id" to "2"
    And I press "list-order-btn" button
    Then I should see "2" in the result
    And I should see "Completed" in the "status" input value


Scenario: Delete an order
    When I visit the "home page"
    And I set the "user_id" to "1"
    And I press "list-order-btn" button
    And I press "delete-order-btn" button
    Then I should see "Success" in the "flash_message"
    When I set the "user_id" to "1"
    And I press "list-order-btn" button
    Then I should see "Success" in the "flash_message"
    And I should see "1" in the result
    And I should see "1670369201" in the result
    And I should see "1670369202" in the result
    And I should see "1670369203" in the result
    And I should not see "1670369200" in the results


Scenario: List item of order
    When I visit the "home page"
    And I set the "user_id" to "23"
    And I press "list-order-btn" button
    And I copy the "order_id" field
    And I press "clear-order-btn" button
    And I paste the "order_id_for_item" field
    And I press "get-item-btn" button
    Then I should see "Success" in the "flash_message"
    And I should see "7" in the item results

Scenario: Add item to order
    When I visit the "home page"
    And I set the "user_id" to "23"
    And I press "list-order-btn" button
    And I copy the "order_id" field
    And I press "clear-order-btn" button
    And I paste the "order_id_for_item" field
    And I set the "item_id" to "2"
    And I press "add-item-btn" button
    Then I should see "Success" in the "flash_message"
    When I press "get-item-btn" button
    Then I should see "Success" in the "flash_message"
    Then I should see "2" in the result

Scenario: Delete item in order
    When I visit the "home page"
    And I set the "user_id" to "23"
    And I press "list-order-btn" button
    And I copy the "order_id" field
    And I press "clear-order-btn" button
    And I paste the "order_id_for_item" field
    And I set the "item_id" to "7"
    And I press "delete-item-btn" button
    # Then I should see "Success" in the "flash_message"
    When I press "get-item-btn" button
    # Then I should see "Success" in the "flash_message"
    Then I should not see "7" in the item results