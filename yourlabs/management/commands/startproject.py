import os
import subprocess
from optparse import make_option

from django.core.management.commands.startproject import Command as BaseCommand

from yourlabs import YOURLABS_TEMPLATE


class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--requirements-file',
                    action='store',
                    default='requirements/base.txt',
                    help='The path to requirements to install.'),
        make_option('--no-install-requirements', action='store_true',
            help='Do NOT install project requirements.'),
        make_option('--no-install-db', action='store_true', default=True,
            help='Do NOT Run syncdb and migrate.'),
        make_option('--no-createsuperuser', action='store_true', default=True,
            help='Do NOT createsuperuser after installing your db.'),
        make_option('--vagrant-up', action='store_true',
            help='Run vagrant after making your project.'),
    )

    def __new__(cls, *args, **kwargs):
        """ Override default for --template option """
        instance = object.__new__(Command, *args, **kwargs)

        for o in instance.option_list:
            if o.dest == 'template':
                o.default = YOURLABS_TEMPLATE
            if o.dest == 'extensions':
                o.default = 'ini,json,md,rst,py,Makefile,sh,conf'

        return instance

    def handle(self, project_name=None, target=None, *args, **options):
        super(Command, self).handle(project_name, target, *args, **options)

        project_path = os.path.join(os.getcwd(), project_name)
        manage_path = os.path.join(project_path, 'manage.py')
        import ipdb; ipdb.set_trace()  # XXX BREAKPOINT

        if not options['no_install_requirements']:
            print '[yl] Installing project requirements ....'
            subprocess.call(['pip', 'install', '--exists-action', 'i', '-r',
                os.path.join( project_path, options['requirements_file'])])

        if not options['no_install_db']:
            print '[yl] Setting up the dev database ....'
            subprocess.call([manage_path, 'syncdb', '--noinput'])
            subprocess.call([manage_path, 'migrate', '--noinput'])

        if not options['no_createsuperuser']:
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
