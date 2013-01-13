############
Sportbooking
############

A system for tracking reservations for the different football fields, pool tables, volleyball fields and tennis courts that FRRyd are responsible for.

Requirements
============

* Python 2.7
* Django 1.4
* `django-hvad <https://github.com/KristianOellegaard/django-hvad>`__
* `django-cas <https://bitbucket.org/cpcc/django-cas/overview>`__
* `Python Imaging Library <http://www.pythonware.com/products/pil>`__

Setup
=====

Make appropriate changes in the file sportbooking_frryd/settings.py. The following must be set up:

* DEBUG = false (no need to change TEMPLATE_DEBUG)
* ADMINS - should contain information for admins.
* DATABASES - must contain appropriate settings for the server's database.
* MEDIA_ROOT - should point to a place on the web server where media files (images) can be placed by django, and accessed by clients of the web server. Make sure the web server can read and write to this directory. This is used for images uploaded via the admin interface.
* MEDIA_URL - the base of the address pointing to the media files, as seen from a client of the web server.
* TEMPLATE_DIRS - must include a full absolute path to the template directory

Ensure that the required database exists. Run ``python manage.py syncdb`` from the project root.

Internationalization
====================

We have to support both English and Swedish, of course (and more languages later if we want!). Our application has two things to internationalize: Static content and dynamic content. Static content is hard-coded into the site, stuff that's being said on pages etc. Dynamic content is translations for stuff that is added to the database, for example bookable resources.

Adding dynamic content
----------------------

When you add dynamic content with the admin interface, it should also be possible to add translations to all relevant languages.

Adding static content
---------------------

If you've added strings that need to be translated (in source), you need to add translations. To do this, first run ``django-admin.py makemessages -a``, then edit the .po files in conf/locale/*/LC_MESSAGES/ and add the translations of the stuff you've added. Then, run ``django-admin.py compilemessages``. Both commands should be run from the root directory of the project.
