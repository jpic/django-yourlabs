from django.core.management.command.startproject import Command as BaseCommand


class Command(BaseCommand):
    def handle(self, app_or_project, name, target=None, **options):
        print 'you have', options['template']
