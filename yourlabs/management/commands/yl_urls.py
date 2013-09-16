from ..templates import TemplateCommand


class Command(TemplateCommand):
    args = '<app_name>'
    help = 'Creates a urls.py skeleton for the given app'
    template_dir = 'urls'

    def handle(self, app_name, command_name, *args, **options):
        self.command_name = command_name

        super(Command, self).handle(app_name, self.template_dir, *args,
                                    **options)
