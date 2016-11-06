######################################################################################################################
# Name: rel_db_downgrade.py
# Description: This script will help to remove the changes done to the upgraded sqllite database.
# Reference: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# Date: 11/2/2016
######################################################################################################################

from migrate.versioning import api
from config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO

v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
api.downgrade(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO, v - 1)
v = api.db_version(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)
print 'Current version of database: '+ str(v)

