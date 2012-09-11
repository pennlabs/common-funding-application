

Setup
=====

* Go to pennapps.com/phpmyadmin and make a new database for yourself by copying an existing one.
* Add a user to the database with root permissions. You will use this to connect to the db.
* Edit /etc/apache2/site-available/default. Search for Common Funding Applications and copy one of the existing settings. Edit it to your match own settings.
* Modify sandbox_config to match the settings that you set up for yourself in the previous steps.
* Run "python manage.py collectstatic -l" to symlink static files (don't forget the "-l" for symlinks).
* Go to /admin and modify the Site object in Sites. Change the domain name to something like "pennapps.com/ceasarb-cfa" and the display name to "The Common Funding App".
