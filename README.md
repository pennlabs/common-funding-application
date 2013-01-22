Common Funding Application
=============================

The [Common Funding Application](http://cfa.pennapps.com) is an online application that allows student groups and organizations to request funding from various funding sources at the [University of Pennsylvania](http://www.upenn.edu).

## Local Setup
* Install [pip](http://www.pip-installer.org/en/latest/installing.html)

* Install python dependencies (`sudo pip install -r requirements.txt`)

* Install [node.js](http://nodejs.org/)

* Install [CoffeeScript](http://coffeescript.org) (`sudo npm install -g coffee-script`)

* Compile the CoffeeScript files (`coffee -o app/static/js/ -c app/static/coffeescripts/` or `cake build` if you are in the app/static directory)

* Create a configuration file (`cp sandbox_config.py_default sandbox_config.py`)

* Fill in missing fields in sandbox_config.py

* Create database (`python manage.py syncdb`)

* Import dummy data (`python import_demo.py`)

* Run the server (`python manage.py runserver`)

* Navigate to the [app](http://localhost:8000/)

## Server Setup

* Go to [pennapps.com/phpmyadmin](http://pennapps.com/phpmyadmin) and make a new database for yourself by copying an existing one.

* Add a user to the database with root permissions (click privileges, add a new user, then check all permissions). You will use this to connect to the db.

* Edit /etc/apache2/sites-available/default. Search for Common Funding Applications and copy one of the existing settings. Edit it to your match own settings.

* Modify sandbox_config to match the settings that you set up for yourself in the previous steps.

* Navigate to app/static and run `coffee -o js/ -c coffeescripts/` to compile the CoffeeScript.

* Run `python manage.py collectstatic -l` to symlink static files (do not forget the "-l" for symlinks).

* Run python import_demo.py

## Front-End Testing

* Navigate to app/static

* Run tests (`cake test`)

## DB migrations

_Note_: instructions are from [our wiki](https://github.com/pennappslabs/wiki/wiki/Setting-Up-South)

* Edit models.py

* _first migration only_ `python manage.py convert_to_south app`

* `python manage.py schemamigration app --auto NAME_OF_CHANGE`

* `python manage.py migrate app`
