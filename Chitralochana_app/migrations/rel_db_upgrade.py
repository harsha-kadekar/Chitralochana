#######################################################################################################################
# Name: rel_db_upgrade.py
# Description: This script will help to upgrade the our existing SQLLite Database to the new version. It uses
#               rel_db_migrate.py generated scripts.
# References: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# Date: 11/2/2016
#######################################################################################################################
from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO

api.upgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'Current database version: ' + str(v)