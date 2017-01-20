import argparse
import os

import unittest
import warnings

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager, Command
from flask_script import prompt_bool

from backend.app.core import app, db, configure_app


warnings.simplefilter('ignore')

parser = argparse.ArgumentParser()
group = parser.add_mutually_exclusive_group()
group.add_argument("-d", "--debug", action="store_true")
group.add_argument("-t", "--test", action="store_true")
args, _ = parser.parse_known_args()

if args.debug:
    configure_app(config="debug")
if args.test:
    configure_app(config="test")

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_option("-d", "--debug",
                   action="store_true", dest="debug", required=False)
manager.add_option("-t", "--test",
                   action="store_true", dest="test", required=False)

# migrations : python manage.py db to show usage
manager.add_command('db', MigrateCommand)


class SeedDB(Command):
    """Seed the db """
    def run(self):
        if args.test:
            raise Exception("Test Database is seed in test case tear up !")
        #some seed method


manager.add_command('seeddb', SeedDB())


class DropDB(Command):
    """drop db """
    def run(self):
        if prompt_bool("Are you sure you want to lose all your data"):
            os.system("python manage.py -t db downgrade base")


manager.add_command('dropdb', DropDB())


class RunTests(Command):
    """Seed the db """
    def run(self):
        configure_app(config="test")
        os.system("python manage.py -t db downgrade base")
        os.system("python manage.py -t db upgrade")
        test_loader = unittest.defaultTestLoader
        test_runner = unittest.TextTestRunner()
        test_suite = test_loader.discover('tests')
        test_runner.run(test_suite)


manager.add_command('runtests', RunTests())

if __name__ == '__main__':
    manager.run()
