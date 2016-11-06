#####################################################################################
# Name: manage.py
# Description: This file is used as the launch script. On running this script we will
#               be starting the web server.
# Reference: Flask Web Development.
# Date: 11/2/2016
#######################################################################################
import os
from app import create_app, rel_db
from app.models import User
from flask_script import Manager, Shell
from flask_migrate import Migrate, MigrateCommand

app = create_app('default')
manager = Manager(app)
migrate = Migrate(app, rel_db)

def make_shell_context():
    return dict(app=app, db=rel_db, User=User)

@manager.command
def test():
    '''
    This will run the unit tests.
    :return: -
    '''
    import unittest
    tests = unittest.TestLoader().discover('tests')
    unittest.TextTestRunner(verbosity=2).run(tests)

manager.add_command("shell", Shell(make_context=make_shell_context()))
manager.add_command('db', MigrateCommand)

if __name__=='__main__':
    manager.run()