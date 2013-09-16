from ..templates import TemplateCommand


class Command(TemplateCommand):
    args = '<app_name>'
    help = 'Creates a urls.py skeleton for the given app'

    def handle(self, app_name, command_name, *args, **options):
        self.command_name = command_name

        super(Command, self).handle(app_name, 'command', extra_context={
            'command_name': command_name}, *args, **options)

    def source_rename(self, source):
        destination = super(Command, self).source_rename(source)
        return destination.replace('command_name', self.command_name)
