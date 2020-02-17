Common Funding Application
=============================

[![CircleCI](https://circleci.com/gh/pennlabs/common-funding-application.svg?style=shield)](https://circleci.com/gh/pennlabs/common-funding-application)
[![Coverage Status](https://codecov.io/gh/pennlabs/common-funding-application/branch/master/graph/badge.svg)](https://codecov.io/gh/pennlabs/common-funding-application)

The [Common Funding Application](https://penncfa.com) is an online application that allows student groups and organizations to request funding from various funding sources at the [University of Pennsylvania](http://www.upenn.edu).

## Local Backend Setup
* Install [pip](https://pip.pypa.io/en/latest/installing/)

* Install `mysql_config` (`apt-get install libmysqlclient-dev`)

* Create a virtualenv (`virtualenv env`) and activate it (`source env/bin/activate`). You will need to re-activate the virtualenv in every new terminal you use.

* Install python dependencies (`pipenv install -d`)

* Migrate database (`python manage.py migrate`)

* Import dummy data (`python import_demo.py`)

* Run the server (`python manage.py runserver`)

* Navigate to the [app](http://localhost:8000/)

## Front-End Setup

* Install [node.js](http://nodejs.org/)

* Install [Mocha](https://mochajs.org/#installation) (`sudo npm install -g mocha`)

* Run tests (`mocha app/static/test/`)

## DB migrations

* Edit models.py

* `python manage.py makemigrations`

* `python manage.py migrate`

## Environment Variables

In development, you do not need to add any environment variables.
However, in production, there are a few that need to be set:

    DEBUG=False
    SENDGRID_USERNAME=pennlabs
    SENDGRID_PASSWORD
    SECRET_KEY
    DATABASE_URL

## Contributors

* The development team at [Penn Labs](https://pennlabs.org/)
