#!/usr/bin/env python
import os
from sqlalchemy import func
from app import create_app, db
from app.models import Hosts
from flask_script import Manager, Shell, Server
from flask_migrate import Migrate, MigrateCommand
from config import config

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)
migrate = Migrate(app, db)


def make_shell_context():
    return dict(app=app, db=db, Hosts=Hosts, func=func)


manager.add_command('shell', Shell(make_context=make_shell_context))
manager.add_command('db', MigrateCommand)
manager.add_command('runserver', Server(host='0.0.0.0'))


@manager.command
def setup():
    print('Checking database')
    env = os.getenv('FLASK_CONFIG') or 'default'
    db_path = config[env].SQLALCHEMY_DATABASE_URI[10:]
    if os.path.isfile(db_path):
        print('Database has already been created!')
        print('Start the server by running "python manage.py runserver"')
    else:
        print('Database not found, creating new database')
        db.create_all()
        print('Database created!')
        print('You can test the server by running "python manage.py runserver"')


if __name__ == '__main__':
    manager.run()
