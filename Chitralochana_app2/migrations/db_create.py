from migrate.versioning import api
from flask import current_app
from app import create_app, db
import os.path

myapp = create_app('development')
app_context = myapp.app_context()
app_context.push()
db.create_all()

if not os.path.exists(current_app.config['SQLALCHEMY_MIGRATE_REPO']):
    api.create(current_app.config['SQLALCHEMY_MIGRATE_REPO'], 'database_repository')
    api.version_control(current_app.config['SQLALCHEMY_DATABASE_URI'], current_app.config['SQLALCHEMY_MIGRATE_REPO'])
else:
    api.version_control(current_app.config['SQLALCHEMY_DATABASE_URI'], current_app.config['SQLALCHEMY_MIGRATE_REPO'], api.version(current_app.config['SQLALCHEMY_MIGRATE_REPO']))