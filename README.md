# Epic Events CRM

## Description

This API allows staff members to manage clients and their associated contracts and events.

## Installation

1. Clone the project repo with <code> git clone https://github.com/Louack/OC_PP10.git </code> or download the project [zip file](https://github.com/Louack/OC_PP12/archive/refs/heads/master.zip).
2. Go in the project directory from the command line
3. Create a virtual env with `$ py -m venv env` for windows or `$ python3 -m venv env` for macos/linux.
4. Activate the virtual env with `$ env\Scripts\activate` for windows or `$ source env/bin/activate` for macos/linux.
5. Install the required packages with `$ pip install -r requirements.txt`.
6. Create a .env file and add the following variables:
   1. DB_NAME = < the name of an empty postgres DB on your system >
   2. DB_USER = < the name of a user with access permission to the DB >
   3. DB_PASSWORD = < your user password >
7. Deploy the migrations files to the database with `$ py manage.py migrate`.
8. Load fixtures with the command `$py manage.py loaddata fixtures/demo_fixtures.json`.
9. The server can finally be launched with `$py manage.py runserver`.

## Features

The API is available at localhost:8000
Postman documentation of all features are available at: !!!TO COMPLETE!!!
Staff members can also log in via the admin panel from (/admin).

## Demo data

The data provided contains 5 users and 1 client with 1 associated contract with is associated event
The users usernames are:
- manager (superuser)
- salesman_01
- salesman_02
- support_01
- support_02

The password for all users is 'crm_project'.

## Testing

Tests can be initiated with `$py manage.py test`.

## Coverage

Testing coverage can be checked with `$coverage run --source='apps' manage.py test` followed by `$coverage report` 

## Linting

The project can be checked with PEP8 recommendations with `$flake8`.
