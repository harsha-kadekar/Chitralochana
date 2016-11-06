###############################################################################################
# Name: rel_db_create.py
# Description: This file has commands/script to create the user database
# References: https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-iv-database
# Date: 11/1/2016
###############################################################################################

from migrate.versioning import api
from flask import current_app
from app import create_app, rel_db
#from config import SQLALCHEMY_DATABASE_URI
#from config import SQLALCHEMY_MIGRATE_REPO
#from app import rel_db
import os.path

myapp = create_app('development')
app_context = myapp.app_context()
app_context.push()
rel_db.create_all()

if not os.path.exists(current_app.config['SQLALCHEMY_MIGRATE_REPO']):
    api.create(current_app.config['SQLALCHEMY_MIGRATE_REPO'], 'database_repository')
    api.version_control(current_app.config['SQLALCHEMY_DATABASE_URI'], current_app.config['SQLALCHEMY_MIGRATE_REPO'])
else:
    api.version_control(current_app.config['SQLALCHEMY_DATABASE_URI'], current_app.config['SQLALCHEMY_MIGRATE_REPO'], api.version(current_app.config['SQLALCHEMY_MIGRATE_REPO']))
    