# NYU DevOps Project Template

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Python](https://img.shields.io/badge/Language-Python-blue.svg)](https://python.org/)

This is a skeleton you can use to start your projects

## Overview

This project template contains starter code for your class project. The `/service` folder contains your `models.py` file for your model and a `routes.py` file for your service. The `/tests` folder has test case starter code for testing the model and the service separately. All you need to do is add your functionality. You can use the [lab-flask-tdd](https://github.com/nyu-devops/lab-flask-tdd) for code examples to copy from.

## Manual Setup

1. Clone this git repository.
2. Open this project in the docker container.
3. Initialize the database by (We recommend this to avoid db error)
   1. Run ```flask db init``` to initialize the migration folder.
   2. Run ```flask db migrate``` to migrate the models to db schema.
   3. Run ```flask db upgrade``` to apply  the schema to database.
4. Run the app by ```flask run``` or ```honcho start```

## RESTful APIs
- ```GET /orders``` 

- ```GET /orders/{order_id}```:  
  * order_id (int): the order id that the user wants to get information about.
  
- ```DELETE /orders/{order_id}/items/{item_id}```:  
  * order_id (int): the order id item from which the user wants to delete from.
  * item_id (int): the item id of the item that the user wants to delete.

- ```GET /orders/{order_id}/items``` 

- ```GET /orders/{order_id}/items/{item_id}```:  
  * order_id (int): the order id which include the item that the user wants to get information about.
  * item_id (int): the item id of the item that the user wants to get information about.
 
- ```DELETE /orders/{order_id}```:  
  * order_id (int): the order id of the item that the user want to delete.

## Contents

The project contains the following:

```text
.gitignore          - this will ignore vagrant and other metadata files
.flaskenv           - Environment variables to configure Flask
.gitattributes      - File to gix Windows CRLF issues
.devcontainers/     - Folder with support for VSCode Remote Containers
dot-env-example     - copy to .env to use environment variables
requirements.txt    - list if Python libraries required by your code
config.py           - configuration parameters

service/                   - service python package
├── __init__.py            - package initializer
├── models.py              - module with business models
├── routes.py              - module with service routes
└── common                 - common code package
    ├── error_handlers.py  - HTTP error handling code
    ├── log_handlers.py    - logging setup code
    └── status.py          - HTTP status constants

tests/              - test cases package
├── __init__.py     - package initializer
├── test_models.py  - test suite for business models
└── test_routes.py  - test suite for service routes
```

## License

Copyright (c) John Rofrano. All rights reserved.

Licensed under the Apache License. See [LICENSE](LICENSE)

This repository is part of the NYU masters class: **CSCI-GA.2820-001 DevOps and Agile Methodologies** created and taught by *John Rofrano*, Adjunct Instructor, NYU Courant Institute, Graduate Division, Computer Science, and NYU Stern School of Business.
