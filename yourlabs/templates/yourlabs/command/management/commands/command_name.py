from optparse import make_option

from django.core.management.base import BaseCommand, CommandError
from django.conf import settings


class Command(BaseCommand):
    args = '<...>'
    help = '...'

    """
    option_list = BaseCommand.option_list + (
        make_option('--template',
            action='store',
            default='',
            help='Delete poll instead of closing it'
        ),
    )
    """

    def handle(self, *args, **options):
        self.verbosity = int(options.get('verbosity'))

        if self.verbosity >= 1:
            print '{{ command_name|title }} complete'
