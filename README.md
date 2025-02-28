Common Funding Application
=============================

[![CircleCI](https://circleci.com/gh/pennlabs/common-funding-application.svg?style=shield)](https://circleci.com/gh/pennlabs/common-funding-application)
[![Coverage Status](https://codecov.io/gh/pennlabs/common-funding-application/branch/master/graph/badge.svg)](https://codecov.io/gh/pennlabs/common-funding-application)

The [Common Funding Application](https://penncfa.com) is an online application that allows student groups and organizations to request funding from various funding sources at the [University of Pennsylvania](http://www.upenn.edu).

## Local Backend Setup
* Install [uv](https://docs.astral.sh/uv/getting-started/installation/)

* Install `mysql_config` (Ubuntu: `apt install libmysqlclient-dev` / MacOS: `brew install mysql-connector-c`)

* Install python dependencies (`uv sync`)

* Migrate database (`uv run manage.py migrate`)

* Import dummy data (`uv run import_demo.py`)

* Run the server (`uv run manage.py runserver`)

* Navigate to the [app](http://localhost:8000/)

* Example login credntials: `philo / philo` for requester, `spectrum / spectrum` for funder

## Front-End Setup

* Install [Bun](https://bun.sh/docs/installation)

* Install [Mocha](https://mochajs.org/#installation) (`bun install -g mocha`)

* Run tests (`mocha app/static/test/`)

## DB migrations

* Edit models.py

* `uv run manage.py makemigrations`

* `uv run manage.py migrate`

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
