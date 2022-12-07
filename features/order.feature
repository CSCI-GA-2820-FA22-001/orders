Feature: The pet store service back-end
    As a User of Order syste
    I need a RESTful catalog service
    So that I can keep track of all my orders and items

Background:
    Given the following orders
    | user_id | create_time | status |
    | 1       | 1670369200  | 1      |
    | 1       | 1670369200  | 1      |
    | 1       | 1670369200  | 1      |
    | 1       | 1670369200  | 1      |

Scenario: The server is running
    When I visit the "Home Page"
    Then I should see "Order Demo RESTful Service" in the title