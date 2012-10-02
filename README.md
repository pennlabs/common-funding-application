

Setup
=====

* Go to [pennapps.com/phpmyadmin](http://pennapps.com/phpmyadmin) and make a new database for yourself by copying an existing one.

* Add a user to the database with root permissions (click privileges, add a new user, then check all permissions). You will use this to connect to the db.

* Edit /etc/apache2/site-available/default. Search for Common Funding Applications and copy one of the existing settings. Edit it to your match own settings.

* Modify sandbox_config to match the settings that you set up for yourself in the previous steps.

* Run `python manage.py collectstatic -l` to symlink static files (do not forget the "-l" for symlinks).

* Navigate to app/static and run `coffee -o js/ -c coffeescripts/` to compile the CoffeeScript.

* Go to /admin and modify the Site object in Sites. Change the domain name to something like "pennapps.com/ceasarb-cfa" and the display name to "The Common Funding App".
