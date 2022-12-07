Feature: The pet store service back-end
    As a User of Order syste
    I need a RESTful catalog service
    So that I can keep track of all my orders and items

Background:
    Given the following orders
        | user_id | create_time | status | items |
        | 1       | 1670369200  | 1      | 1,2   |
        | 1       | 1670369200  | 1      | 3,4   |
        | 1       | 1670369200  | 1      | 5     |
        | 1       | 1670369200  | 1      | 6     |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order Demo RESTful Service" in the title

Scenario: List orders of a user
    When I visit the "Home Page"
    And I set the "user_id" to "1"
    And I press "list-order-btn" button
    Then I should see "Success" in the "flash_message"