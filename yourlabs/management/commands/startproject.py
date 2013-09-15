import os
import subprocess
from optparse import make_option

from django.core.management.commands.startproject import Command as BaseCommand

from yourlabs import YOURLABS_TEMPLATE


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--local', action='store_true',
            help='Prepare for local development, alias for '
                '--install-requirements, --install-db and --createsuperuser'),
        make_option('--vagrant', action='store_true',
            help='Prepare for vagrant server, alias for --vagrant-up'),
        make_option('--install-requirements', action='store_true',
            help='Install project requirements.'),
        make_option('--install-db', action='store_true',
            help='Prepare the dev sqlite db with syncdb and migrate.'),
        make_option('--createsuperuser', action='store_true',
            help='Run createsuperuser after installing your db.'),
        make_option('--vagrant-up', action='store_true',
            help='Run vagrant after making your project.'),
        make_option('--requirements-file',
                    action='store',
                    default='requirements/base.txt',
                    help='The path to requirements to install.'),
    )

    def __new__(cls, *args, **kwargs):
        """ Override default for --template option """
        instance = object.__new__(Command, *args, **kwargs)

        for o in instance.option_list:
            if o.dest == 'template':
                o.default = YOURLABS_TEMPLATE
            if o.dest == 'extensions':
                o.default = ['ini', 'json', 'md', 'rst', 'py', 'Makefile',
                             'sh', 'conf']

        return instance

    def handle(self, project_name=None, target=None, *args, **options):
        super(Command, self).handle(project_name, target, *args, **options)

        project_path = os.path.join(os.getcwd(), project_name)
        manage_path = os.path.join(project_path, 'manage.py')

        if options['local']:
            options['install_requirements'] = True
            options['install_db'] = True
            options['createsuperuser'] = True

        if options['vagrant']:
            options['vagrant_up'] = True

        if options['install_requirements']:
            print '[yl] Installing project requirements ....'
            subprocess.call(['pip', 'install', '--exists-action', 'i', '-r',
                os.path.join( project_path, options['requirements_file'])])

        if options['install_db']:
            print '[yl] Setting up the dev database ....'
            subprocess.call([manage_path, 'syncdb', '--noinput'])
            subprocess.call([manage_path, 'migrate', '--noinput'])

        if options['createsuperuser']:
            print '[yl] Creating a superuser with username=test and'
            print '[yl] email=test@example.com, type in password and enter'
            print '[yl] or exit with Ctrl+C'

            try:
                subprocess.call([manage_path, 'createsuperuser',
                    '--username=test', '--email=test@example.com'])
            except KeyboardInterrupt:
                print 'Superuser creation aborded'

        if options['vagrant_up']:
            os.chdir(project_path)
            subprocess.call(['vagrant', 'up'])
