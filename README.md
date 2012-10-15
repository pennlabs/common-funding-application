Common Funding Application
=============================

## Setup

* Go to [pennapps.com/phpmyadmin](http://pennapps.com/phpmyadmin) and make a new database for yourself by copying an existing one.

* Add a user to the database with root permissions (click privileges, add a new user, then check all permissions). You will use this to connect to the db.

* Edit /etc/apache2/sites-available/default. Search for Common Funding Applications and copy one of the existing settings. Edit it to your match own settings.

* Modify sandbox_config to match the settings that you set up for yourself in the previous steps.

* Run `python manage.py collectstatic -l` to symlink static files (do not forget the "-l" for symlinks).

* Navigate to app/static and run `coffee -o js/ -c coffeescripts/` to compile the CoffeeScript.

* Run python import_demo.py


## DB migrations

_Note_: instructions are from [our wiki](https://github.com/pennappslabs/wiki/wiki/Setting-Up-South)

* Edit models.py

* _first migration only_ `python manage.py convert_to_south app`

* `python manage.py schemamigration app --auto NAME_OF_CHANGE`

* `python manage.py migrate app`
