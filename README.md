Common Funding Application
=============================

The [Common Funding Application](https://penncfa.com) is an online application that allows student groups and organizations to request funding from various funding sources at the [University of Pennsylvania](http://www.upenn.edu).

## Local Setup
* Install [pip](http://www.pip-installer.org/en/latest/installing.html)

* Install python dependencies (`sudo pip install -r requirements.txt`)

* Install [node.js](http://nodejs.org/)

* Install [CoffeeScript](http://coffeescript.org) (`sudo npm install -g coffee-script`)

* Compile the CoffeeScript files (`coffee -o app/static/js/ -c app/static/coffeescripts/` or `cake build` if you are in the app/static directory)

* Create a configuration file (`cp sandbox_config.py_default sandbox_config.py`)

* Fill in missing fields in sandbox_config.py

* Create database (`python manage.py syncdb`)

* Migrate database (`python manage.py migrate`)

* Import dummy data (`python import_demo.py`)

* Run the server (`python manage.py runserver`)

* Navigate to the [app](http://localhost:8000/)

## Front-End Testing

* Navigate to app/static

* Run tests (`cake test`)

## DB migrations

_Note_: instructions are from [our wiki](https://github.com/pennlabs/wiki/wiki/Setting-Up-South)

* Edit models.py

* _first migration only_ `python manage.py convert_to_south app`

* `python manage.py schemamigration app --auto NAME_OF_CHANGE`

* `python manage.py migrate app`

## Contributors

* The development team at [Penn Labs](http://pennlabs.org/#team)
